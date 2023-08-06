import argparse
import os
import sys

import matplotlib.pyplot as plt
import torch
import torch.optim as optim
from sysflow.utils.common_utils.file_utils import dump, load 
from hpman.m import _
import wandb

import hpargparse
import networks
import utils
from utils import *

class neuralsampler: 
    def __init__(self): 
        # save the params 
        device = torch.device("cuda:" + str(0) if torch.cuda.is_available() else "cpu")

        # hid_dim = _("hid_dim", 100)  # noise dimension

        D = networks.SmallMLP(dim, n_hid=hid_dim, n_out=1)
        G = networks.SmallMLP(dim, n_hid=hid_dim, n_out=1)

        D.to(device)
        G.to(device)

        logger.info(D)
        logger.info(G)

        G_optimizer = optim.Adam(
            G.parameters(), lr=args.lr, weight_decay=args.weight_decay, betas=(0.9, 0.999)
        )
        D_optimizer = optim.Adam(
            D.parameters(),
            lr=args.lr,
            betas=(0.9, 0.999),
            weight_decay=args.critic_weight_decay,
        )

        #region pack the params
        self.device = device
        self.D = D
        self.G = G
        self.G_optimizer = G_optimizer
        self.D_optimizer = D_optimizer
        #endregion

    def train(self): 

        #region unpack the params
        device = self.device
        D = self.D
        G = self.G
        G_optimizer = self.G_optimizer
        D_optimizer = self.D_optimizer
        #endregion

        G.train()
        D.train()

        G_sample_list = []

        X_list = []
        Y_list = []
        Z_list = []

        # adding the data with the model name 
        data_dict = load('stein-gan.pkl')

        X, Y = data_dict['x'], data_dict['y']

        # trainer the network
        for itr in range(args.niters):

            G_optimizer.zero_grad()
            D_optimizer.zero_grad()


            # load the initial dataset // or create the initial dataset 

            # x ~ U(-2, 1)
            # y ~ U(-0.5, 2.5)
            # z0 = np.random.uniform(-2, 1, size=[args.batch_size, 2])
            # z0[:, 1] += 1.5 
            
            idx = np.random.choice(len(X), args.batch_size)
            x = X[idx]
            y = Y[idx]

            # = np.random.uniform(-2, 1, size=[args.batch_size, 2])

            # the density of mu is 1 / 64 

            x = torch.tensor(x, requires_grad=True).float().cuda()
            y = torch.tensor(y, requires_grad=True).float().cuda()


            # z0 = sample_z(args.batch_size, z_dim, std=2).to(device)


            G_sample = x
            # compute dlogp(x)/dx

            potential = G(x)

            ratio = torch.exp( potential ) 

            # so here the ratio has nothing do with the mu ? 
            ratio = ratio / ratio.mean()

            # care about the samples later 
            # index = np.random.choice(10000, 2000)
            # G_sample = torch.tensor(Ngaussian.X_new[index], dtype=torch.float32, requires_grad=True).cuda()

            # normalization outside for mmd ? 
            # beta for mmd ? 


            # 2 gan formulas
            # 2 mmd formula [x8] [combine with the two method] (mmd, mmd_2sample, mmd outside, mmd_2sample outside)

            # different method 
            # method I

            D_fake = D(x) - D(y)

            # method II
            D_fake_jacob = keep_grad(  D(x).sum(), x)

                     

            # Lf = Delta f + b(x) grad f 
            stats = D_fake 
            stats *= ratio


            loss = stats.mean()  # estimate of S(p, q)

            # two way for the l2 penalty 
            # zero or one 

            l2_penalty = (D_fake_jacob * D_fake_jacob).sum(1).mean() * args.l2  # penalty to enforce f \in F

            # l2_penalty = ( torch.norm(D_fake_jacob, dim=1) -1  ).square().mean() * args.l2  # penalty to enforce f \in F


            # adversarial!
            if args.d_iters > 0 and itr % (args.g_iters + args.d_iters) < args.d_iters : 
                (-1.0 * loss + l2_penalty).backward()
                D_optimizer.step()

            else:
                loss.backward()
                G_optimizer.step()


            new_dict = { 
                'Discriminator': tc( -1.0 * loss + l2_penalty ), 
                'Generator': tc( loss ), 
                # 'grad f':  tc( sq_fx.mean()), 
                # 'laplace f':  tc( tr_dfdx.mean()), 
                'l2 penalty': tc(l2_penalty), 
            }

            wandb.log(new_dict)

            if itr % args.viz_freq == 0:

                x = np.arange(-4.0, 4.0, 0.1)
                y = np.arange(-4.0, 4.0, 0.1)
                # x = np.arange(-2, 1, 0.04)
                # y = np.arange(-0.5, 2.5, 0.04)

                _X, _Y = np.meshgrid(x, y)

                z0 = np.concatenate([_X.reshape(-1, 1), _Y.reshape(-1, 1)], axis=1)

                z0 = torch.tensor(z0, requires_grad=True).float().cuda()

                potential = G(z0)


                potential = tc(potential)

                exp_pot = np.exp( potential )

                prob = exp_pot / exp_pot.mean() * 64

                Z = prob.reshape(len(_X), len(_X[0]))

                fig, ax = plt.subplots(figsize=(6,6))

                X_list.append(_X)
                Y_list.append(_Y)
                Z_list.append(Z)

                print(itr)
            

        new_dict = { 
            'X': X_list, 
            'Y': Y_list, 
            'Z': Z_list, 
        }


        # change the name below 
        dump(new_dict, 'NS-gaussian20.pkl')



# if __name__ == "__main__":
    # wandb.init(project="neuralsampler", entity="jimmy-math")

    # # this code is trying to reproduce the code of Stein-NS
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--niters", type=int, default=10000)
    # parser.add_argument("--batch_size", type=int, default=2000)
    # parser.add_argument("--lr", type=float, default=3e-4)
    # parser.add_argument("--weight_decay", type=float, default=0)
    # parser.add_argument("--critic_weight_decay", type=float, default=0)
    # parser.add_argument("--save", type=str, default="data/test_steinNS")
    # parser.add_argument("--viz_freq", type=int, default=1000)

    # parser.add_argument("--d_iters", type=int, default=5)
    # parser.add_argument("--g_iters", type=int, default=1)

    # parser.add_argument("--l2", type=float, default=10.0)
    # parser.add_argument("--exact_trace", action="store_false")
    # parser.add_argument("--vector", action="store_true")


    # # parse everything in this directory
    # BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    # _.parse_file(BASE_DIR)  # <-- IMPORTANT

    # # _.parse_file(__file__)

    # hpargparse.bind(parser, _)
    # args = parser.parse_args()

    # wandb.config.update(args) # adds all of the arguments as config variables

    # # logger
    # utils.makedirs(args.save)
    # logger = utils.get_logger(
    #     logpath=os.path.join(args.save, "logs"), filepath=os.path.abspath(__file__)
    # )
    # logger.info(args)

    # cmd_line = 'python ' + ' '.join(sys.argv)
    # logger.info(cmd_line)


    # r = _("r", 15.0)  # radius of the circle where modes on (equally spaced)
    # sd = _("sd", 1.0)  # variance of each component
    # n_comp = _("n_comp", 8)  # number of mixture component (number of modes)
    # z_dim = _("z_dim", 5)  # noise dimension

    # lr_D = _("lr_D", 1e-4)

    # out_dim = _('out_dim', 2)


    # # define the name for the dataset 

    # # choice: gaussian, dw, mb 
    # model = _('model', 'mb')
    # dim = _("dim", 2)  # dimension of the target distribution

    # # use these two params, one can get the dataset 






    # ns = neuralsampler()
    # # training 
    # ns.train()

    # # plot 
    # ns.plot()



