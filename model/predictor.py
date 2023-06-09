import torch

model = torch.hub.load('pytorch/vision:v0.10.0', 'googlenet', pretrained=True)
model.eval()
model.fc = torch.nn.Linear(1024, 116)
model.load_state_dict(torch.load('model/model_state', map_location=torch.device('cpu')))