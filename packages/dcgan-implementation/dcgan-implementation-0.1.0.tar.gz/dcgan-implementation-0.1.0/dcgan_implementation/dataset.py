import tensorflow as tf

BUFFER_SIZE = 60000
BATCH_SIZE = 256



def make_dataset(img_size: int, data_folder: str, channel_count: int):
    def load(file):

        img_data = tf.io.read_file(file)
        img = tf.io.decode_image(
            img_data,
            channels=channel_count,
            expand_animations=False,
            dtype=tf.float32,
        )

        if img.shape[0] != img_size:
            return tf.image.resize(img, [img_size, img_size])
        else:
            return img

    def normalize_a(x):
        return (x - 0.5) / 0.5

    def normalize_b(x):
        return (x - 127.5) / 127.5

    if not data_folder:
        (train_images, _), (_, _) = tf.keras.datasets.mnist.load_data()
        train_images = tf.expand_dims(train_images, axis=-1)
        train_images = tf.image.resize(train_images, [img_size, img_size]).numpy()
        train_images = train_images.reshape(
            train_images.shape[0], img_size, img_size, 1
        ).astype("float32")
        train_dataset = tf.data.Dataset.from_tensor_slices(train_images)
        train_dataset = train_dataset.batch(BATCH_SIZE)
        train_dataset = train_dataset.map(
            normalize_b, num_parallel_calls=tf.data.AUTOTUNE, deterministic=False
        )

    else:
        ds = tf.data.Dataset.list_files(f"{data_folder}*")
        train_dataset = ds.map(
            load, num_parallel_calls=tf.data.AUTOTUNE, deterministic=False
        )
        train_dataset = train_dataset.batch(BATCH_SIZE)
        train_dataset = train_dataset.map(
            normalize_a, num_parallel_calls=tf.data.AUTOTUNE, deterministic=False
        )


    # train_dataset = train_dataset.cache()
    return train_dataset.prefetch(tf.data.AUTOTUNE)