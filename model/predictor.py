import torch

model = torch.hub.load('pytorch/vision:v0.10.0', 'googlenet', pretrained=True)
model.load_state_dict(torch.load('model', map_location=torch.device('cpu')))
