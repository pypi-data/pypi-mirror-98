import glob
import imageio
import matplotlib.pyplot as plt
import tensorflow as tf
import io
import os
from dcgan import IMAGE_DIR


def make_gif():
    anim_file = "dcgan.gif"

    with imageio.get_writer(anim_file, mode="I") as writer:
        filenames = glob.glob("image*.png")
        filenames = sorted(filenames)
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
        image = imageio.imread(filename)
        writer.append_data(image)


def plot_to_image(figure):
    """Converts the matplotlib plot specified by 'figure' to a PNG image and
    returns it. The supplied figure is closed and inaccessible after this call."""
    # Save the plot to a PNG in memory.
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    # Closing the figure prevents it from being displayed directly inside
    # the notebook.
    plt.close(figure)
    buf.seek(0)
    # Convert PNG buffer to TF image
    image = tf.image.decode_png(buf.getvalue(), channels=4)
    # Add the batch dimension
    image = tf.expand_dims(image, 0)
    return image


def show_dataset(dataset, num_examples, summary_writer, **kwargs):

    fig = plt.figure(figsize=(4, 4))

    for i, img in enumerate(dataset.take(num_examples)):
        plt.subplot(4, 4, i + 1)
        plt.imshow(img[i, :, :, :] * 0.5 + 0.5, cmap="gray")
        plt.axis("off")

    plt.show()

    with summary_writer.as_default():
        tf.summary.image("Ground truth", plot_to_image(fig), step=1)


def generate_and_save_images(model, epoch, test_input, summary_writer):
    # Notice `training` is set to False.
    # This is so all layers run in inference mode (batchnorm).

    predictions = model(test_input, training=False)

    fig = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i + 1)
        plt.imshow(predictions[i, :, :, :] * 0.5 + 0.5, cmap="gray")
        plt.axis("off")
    plt.savefig(os.path.join(IMAGE_DIR, "epoch_{:04d}.png".format(epoch)))
    plt.show()

    if epoch % 5 == 0:
        with summary_writer.as_default():
            tf.summary.image(
                "Epoch {:04d}".format(epoch),
                plot_to_image(fig),
                step=epoch,
            )
