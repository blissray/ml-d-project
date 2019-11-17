from models import model
from data_load import get_dataset
from tensorflow.keras import optimizers
from tensorflow.keras import losses

if __name__ == "__main__":

    epochs = 100

    dataset = get_dataset()
    print(dataset )
    model = model()
    print(model.summary())

    loss_object = losses.SparseCategoricalCrossentropy()




    learning_rate = 0.00001
    beta_1 = 0.9
    beta_2 = 0.99
    epsilon = 0.00001
    epochs = 100


    optimizer = optimizers.Adam(learning_rate, beta_1, beta_2, epsilon)

    model.compile(loss=loss_object,
                 optimizer=optimizer ,
                 metrics=['acc'])

    # from tensorflow.keras.callbacks import EarlyStopping
    # early_stopping = EarlyStopping(patience=10, restore_best_weights=True, monitor="val_accuracy")


    model.fit(dataset, epochs=epochs)

