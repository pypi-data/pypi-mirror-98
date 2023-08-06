import tensorflow as tf
import datetime
from dcgan import CHECKPOINT_DIR


fake_out = tf.keras.metrics.Mean(name="gen")
real_out = tf.keras.metrics.Mean(name="desc")
gen_loss_metric = tf.keras.metrics.Mean(name="gen_loss_metric")
disc_loss_metric = tf.keras.metrics.Mean(name="disc_loss_metric")


def make_summary_writer(logname):

    current_time = datetime.datetime.now().strftime("%Y%m%d")
    train_log_dir = f"/home/andy/logs/DCGAN/{current_time}/" + logname
    print(f"Logging metrics to: {train_log_dir}")
    return tf.summary.create_file_writer(train_log_dir)


def record_metrics(step: int, summary_writer):

    with summary_writer.as_default():
        tf.summary.scalar("Discriminator evaluates fake", fake_out.result(), step=step)
        tf.summary.scalar("Discriminator evaluates real", real_out.result(), step=step)
        tf.summary.scalar("Generator loss", gen_loss_metric.result(), step=step)
        tf.summary.scalar("Discriminator loss", disc_loss_metric.result(), step=step)
