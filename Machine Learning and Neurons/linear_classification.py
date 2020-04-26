# -*- coding: utf-8 -*-
"""Linear Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s3yysNspw31FXsZM1Oz41A0KTpzcvY1F
"""

# Import the relevant modules
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the data
data = load_breast_cancer()

# Check data properties
print("Type:", type(data))

print("Keys:", data.keys()) # Shows the keys of the data
print("Shape:", data.data.shape) # Check the shape of X
print("Targets:", data.target.shape) # Check the shape of Y
print("Feature Names:", data.feature_names) # Print the input feature names
print("Targets Names:", data.target_names)

# We split the data into train and test data
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size = 0.33)
N, D = X_train.shape

# We scale the data
# StandardScaler is used for normalizing the data
# This is to prevent inputs from having very different ranges

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)

# We build the model
# Sigmoid to make sure the output is 0/1 

model = nn.Sequential(
    nn.Linear(D, 1),
    nn.Sigmoid()
)

# Loss and optimizer

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters())

# We convert the data into Torch Tensors
X_train = torch.from_numpy(X_train.astype(np.float32))
X_test = torch.from_numpy(X_test.astype(np.float32))

# Targets are reshaped to be 2D arrays of shape Nx1
y_train = torch.from_numpy(y_train.astype(np.float32).reshape(-1, 1))
y_test = torch.from_numpy(y_test.astype(np.float32).reshape(-1, 1))

# Train the model
number_epochs = 2000
train_losses = np.zeros(number_epochs)
test_losses = np.zeros(number_epochs)

for iteration in range(number_epochs):

    # We train the model
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

    # We are also interested in the test/validation loss, to make sure we are not overtiffing
    outputs_test = model(X_test)
    loss_test = criterion(outputs_test, y_test)

    # We save the losses
    train_losses[iteration] = loss.item()
    test_losses[iteration] = loss_test.item()

    if (iteration+1) % 50 == 0:
        print("Epoch: {}/{}, Train Loss: {}, Test Loss: {}".format(iteration+1, number_epochs, loss.item(), loss_test.item()))

# Plot the train and test losses
plt.plot(train_losses, label='train')
plt.plot(test_losses, label='test')
plt.legend()
plt.show()

# Get the accuracy
with torch.no_grad():
    p_train = model(X_train) # Calculate the prediction
    p_train = np.round(p_train.numpy()) # convert tensors to np, and round them
    train_accuracy = np.mean(y_train.numpy() == p_train) # point-wise comparison and take the mean

    p_test = model(X_test)
    p_test = np.round(p_test.numpy())
    test_accuracy = np.mean(y_test.numpy() == p_test)

print('Train Accuracy: {}, Test Accuracy: {}'.format(train_accuracy, test_accuracy))

# Look at the state dict
# This is an ordered dictionary containing the parameters of the model

model.state_dict()

# Save the model
torch.save(model.state_dict(), 'LinearClassification.pt')

# Load the model
model2 = nn.Sequential(
    nn.Linear(D, 1),
    nn.Sigmoid()
)

model2.load_state_dict(torch.load('LinearClassification.pt'))

# Evaluate the model
with torch.no_grad():
    p_train = model2(X_train) # Calculate the prediction
    p_train = np.round(p_train.numpy()) # convert tensors to np, and round them
    train_accuracy = np.mean(y_train.numpy() == p_train) # point-wise comparison and take the mean

    p_test = model2(X_test)
    p_test = np.round(p_test.numpy())
    test_accuracy = np.mean(y_test.numpy() == p_test)

print('Train Accuracy: {}, Test Accuracy: {}'.format(train_accuracy, test_accuracy))
