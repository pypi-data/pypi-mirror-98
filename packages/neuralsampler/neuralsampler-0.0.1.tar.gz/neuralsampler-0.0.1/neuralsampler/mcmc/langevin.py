import numpy as np 

class langevin:
    # perform the over-damped langevin update
    def __init__(self, delta_t, model, batchsize):
        self.delta_t = delta_t
        self.model = model 
        self.k = np.sqrt(2 * delta_t)
        self.batchsize = batchsize
    
    def step(self, x):
        # one step update
        out = x - self.delta_t * self.model.grad(x) + self.k * np.random.randn(self.batchsize, 2)
        return out 
    
    def restrict_step(self, x, thres_eng=100):
        # update with restriction 
        # for example, energy restriction (thres_eng)
        x_new = self.step(x)
        energy_new = self.model.energy(x_new)
        # criterion: x[energy_new < thres_eng]
        out = np.where(energy_new.reshape(-1, 1) < thres_eng, x_new, x)
        return  out 
