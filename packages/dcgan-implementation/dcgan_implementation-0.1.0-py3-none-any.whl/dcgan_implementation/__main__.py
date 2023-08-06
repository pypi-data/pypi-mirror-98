import fire
import os
import tensorflow as tf

import matplotlib.pyplot as plt
import os
import time
import datetime

from dcgan.discriminator import make_discriminator_model, discriminator_loss
from dcgan.generator import make_generator_model, generator_loss
from dcgan.dataset import make_dataset

from dcgan.utils import *
from dcgan.metrics import *
from dcgan import CHECKPOINT_DIR, MODEL_DIR

try:
    from IPython import display
except:
    pass


@tf.function
def train_step(
    images,
    epoch,
    summary_writer,
    generator,
    discriminator,
    generator_optimizer,
    discriminator_optimizer,
):
    noise = tf.random.normal([256, 100])
    # tf.random.gau
    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(noise, training=True)

        real_output = discriminator(images, training=True)
        fake_output = discriminator(generated_images, training=True)

        gen_loss = generator_loss(fake_output)
        # gen_loss = tf.vectorized_map(generator_loss, fake_output)
        # disc_loss = tf.vectorized_map(discriminator_loss, fake_output)
        disc_loss = discriminator_loss(real_output, fake_output)

        gen_loss_metric.update_state(gen_loss)
        disc_loss_metric.update_state(disc_loss)
        fake_out.update_state(fake_output[0])
        real_out.update_state(real_output[0])

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)

    gradients_of_discriminator = disc_tape.gradient(
        disc_loss, discriminator.trainable_variables
    )
    generator_optimizer.apply_gradients(
        zip(gradients_of_generator, generator.trainable_variables)
    )
    discriminator_optimizer.apply_gradients(
        zip(gradients_of_discriminator, discriminator.trainable_variables)
    )

    record_metrics(epoch, summary_writer)


def train(epochs, logname, channels=1, batch_size=256, data_folder=None):

    tf.profiler.experimental.server.start(6009)

    generator = make_generator_model(32, channels)
    discriminator = make_discriminator_model(32, channels)
    generator_optimizer = tf.keras.optimizers.Adam(1e-04, beta_1=0.5)
    discriminator_optimizer = tf.keras.optimizers.Adam(1e-04, beta_1=0.5)

    checkpoint = tf.train.Checkpoint(
        step=tf.Variable(1),
        generator_optimizer=generator_optimizer,
        discriminator_optimizer=discriminator_optimizer,
        generator=generator,
        discriminator=discriminator,
    )

    manager = tf.train.CheckpointManager(checkpoint, CHECKPOINT_DIR, max_to_keep=3)
    summary_writer = make_summary_writer(logname)

    dataset = make_dataset(32, data_folder, channels)

    show_dataset(dataset, 16, summary_writer)
    checkpoint.restore(manager.latest_checkpoint)
    if manager.latest_checkpoint:

        print("Restored from {}".format(manager.latest_checkpoint))
        current_step = int(checkpoint.step.numpy())
        print(
            f"Continuing from epoch {current_step} + {epochs} -> {epochs + current_step}"
        )
        epochs = range(current_step, epochs + current_step)
    else:
        epochs = range(epochs)
        print("Initializing from scratch.")

    for epoch in epochs:
        seed = tf.random.normal([16, 100])
        start = time.time()
        fake_out.reset_states()
        real_out.reset_states()
        gen_loss_metric.reset_states()
        disc_loss_metric.reset_states()

        for step, img_batch in enumerate(dataset.take(256)):
            train_step(img_batch, epoch, summary_writer, generator, discriminator, generator_optimizer, discriminator_optimizer)

        display.clear_output(wait=True)
        generate_and_save_images(generator, epoch + 1, seed, summary_writer)

        checkpoint.step.assign_add(1)
        if int(checkpoint.step) % 15 == 0:
            save_path = manager.save()
            print(
                "Saved checkpoint for step {}: {}".format(
                    int(checkpoint.step), save_path
                )
            )

            # Produce images for the GIF as we go

        print("Time for epoch {} is {} sec".format(epoch + 1, time.time() - start))

    # Generate after the final epoch
    display.clear_output(wait=True)
    generate_and_save_images(generator, epochs, seed, summary_writer)

    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    generator.save(os.path.join(MODEL_DIR, f"gen_trained_{current_time}"))
    discriminator.save(os.path.join(MODEL_DIR, f"disc_trained_{current_time}"))


def fire_():
    fire.Fire(train)
