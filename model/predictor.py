import torch
import torch.nn as nn
import torchvision

# gender predictor

model_age = torch.hub.load('pytorch/vision:v0.10.0', 'googlenet', pretrained=True)

model_age.eval()
model_age.fc = torch.nn.Linear(1024, 116)
model_age.load_state_dict(torch.load('model/model_states/model_state_age', map_location=torch.device('cpu')))

# attractiveness predictor

model_beaty = torchvision.models.vgg19()

new_classifier = nn.Sequential(
    nn.Linear(25088, 4096, bias=True),
    nn.ReLU(inplace=True),
    nn.Dropout(p=0.5, inplace=False),
    nn.Linear(4096, 4096, bias=True),
    nn.ReLU(inplace=True),
    nn.Dropout(p=0.5, inplace=False),
    nn.Linear(4096, 5, bias=True)
)

model_beaty.eval()
model_beaty.classifier = new_classifier
model_beaty.load_state_dict(torch.load('model/model_states/model_state_beaty', map_location=torch.device('cpu')))
