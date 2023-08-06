[![](https://travis-ci.org/kaelzhang/torch-model.svg?branch=master)](https://travis-ci.org/kaelzhang/torch-model)
[![](https://codecov.io/gh/kaelzhang/torch-model/branch/master/graph/badge.svg)](https://codecov.io/gh/kaelzhang/torch-model)
[![](https://img.shields.io/pypi/v/torch-model.svg)](https://pypi.org/project/torch-model/)
[![](https://img.shields.io/pypi/l/torch-model.svg)](https://github.com/kaelzhang/torch-model)

# torch-model

Keras-like torch module wrapper

Tested with Torch 1.8.0

## Install

```sh
$ pip install torch-model
```

## Usage

```py
from torch_model import Model
from torch_model.callbacks import EarlyStopping

model = Model(MyPyTorchModule())

model.compile(
    loss='mse',
    optimizer='adam',
    metrics=['mae', 'mape']
)

history = model.fit(
    train_ds,
    validation_data=val_ds,
    callbacks=[
        EarlyStopping(monitor='val_loss', patience=5)
    ]
)

# The original torch module
model.module
```

## License

[MIT](LICENSE)
