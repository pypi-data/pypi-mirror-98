
import pyro
import pyro.distributions as dist
import torch

import torch.distributions.constraints as constraints

from pyro.infer import SVI, Trace_ELBO, EmpiricalMarginal, TraceEnum_ELBO
from pyro.infer.mcmc import MCMC, NUTS
from pyro.optim import Adam, SGD 

import pyro.contrib.autoguide as autoguide 

import pandas as pd 

from functools import partial

class OneParamLog:
    """1PL IRT model"""
    def __init__(self, priors, device, num_items, num_models, verbose=False):
        if priors not in ['vague', 'hierarchical']:
            raise ValueError("Options for priors are vague and hierarchical")
        if device not in ['cpu', 'gpu']:
            raise ValueError("Options for device are cpu and gpu")
        if num_items <= 0:
            raise ValueError("Number of items must be greater than 0")
        if num_models <= 0:
            raise ValueError("Number of subjects must be greater than 0")
        self.priors = priors
        self.device = device
        self.num_items = num_items
        self.num_models = num_models
        self.verbose = verbose 

        
    def model_vague(self, models, items, obs):
        """Initialize a 1PL model with vague priors"""
        with pyro.plate('thetas', self.num_models, device=self.device):
            ability = pyro.sample('theta', dist.Normal(torch.tensor(0., device=self.device), torch.tensor(1., device=self.device))) 

        with pyro.plate('bs', self.num_items, device=self.device):
            diff = pyro.sample('b', dist.Normal(torch.tensor(0., device=self.device), torch.tensor(1.e3, device=self.device)))

        with pyro.plate('observe_data', obs.size(0), device=self.device):
            pyro.sample("obs", dist.Bernoulli(logits=ability[models] - diff[items]), obs=obs)

            
    def guide_vague(self, models, items, obs):
        """Initialize a 1PL guide with vague priors"""
        # register learnable params in the param store
        m_theta_param = pyro.param("loc_ability", torch.zeros(self.num_models, device=self.device))
        s_theta_param = pyro.param("scale_ability", torch.ones(self.num_models, device=self.device),
                            constraint=constraints.positive)
        m_b_param = pyro.param("loc_diff", torch.zeros(self.num_items, device=self.device))
        s_b_param = pyro.param("scale_diff", torch.empty(self.num_items, device=self.device).fill_(1.e3),
                                constraint=constraints.positive)

        # guide distributions
        with pyro.plate('thetas', self.num_models, device=self.device):
            dist_theta = dist.Normal(m_theta_param, s_theta_param)
            pyro.sample('theta', dist_theta)
        with pyro.plate('bs', self.num_items, device=self.device):
            dist_b = dist.Normal(m_b_param, s_b_param)
            pyro.sample('b', dist_b)


    def model_hierarchical(self, models, items, obs):
        """Initialize a 1PL model with hierarchical priors"""
        mu_b = pyro.sample('mu_b', dist.Normal(torch.tensor(0., device=self.device), torch.tensor(1.e6, device=self.device)))
        u_b = pyro.sample('u_b', dist.Gamma(torch.tensor(1., device=self.device), torch.tensor(1., device=self.device)))
        mu_theta = pyro.sample('mu_theta', dist.Normal(torch.tensor(0., device=self.device), torch.tensor(1.e6, device=self.device)))
        u_theta = pyro.sample('u_theta', dist.Gamma(torch.tensor(1., device=self.device), torch.tensor(1., device=self.device)))
        with pyro.plate('thetas', self.num_models, device=self.device):
            ability = pyro.sample('theta', dist.Normal(mu_theta, 1. / u_theta))
        with pyro.plate('bs', self.num_items, device=self.device):
            diff = pyro.sample('b', dist.Normal(mu_b, 1. / u_b))
        with pyro.plate('observe_data', obs.size(0)):
            pyro.sample("obs", dist.Bernoulli(logits=ability[models] - diff[items]), obs=obs)

            
    def guide_hierarchical(self, models, items, obs):
        """Initialize a 1PL guide with hierarchical priors"""
        loc_mu_b_param = pyro.param('loc_mu_b', torch.tensor(0., device=self.device))
        scale_mu_b_param = pyro.param('scale_mu_b', torch.tensor(1.e2, device=self.device), 
                                constraint=constraints.positive)
        loc_mu_theta_param = pyro.param('loc_mu_theta', torch.tensor(0., device=self.device))
        scale_mu_theta_param = pyro.param('scale_mu_theta', torch.tensor(1.e2, device=self.device),
                            constraint=constraints.positive)
        alpha_b_param = pyro.param('alpha_b', torch.tensor(1., device=self.device),
                        constraint=constraints.positive)
        beta_b_param = pyro.param('beta_b', torch.tensor(1., device=self.device),
                        constraint=constraints.positive)
        alpha_theta_param = pyro.param('alpha_theta', torch.tensor(1., device=self.device),
                        constraint=constraints.positive)
        beta_theta_param = pyro.param('beta_theta', torch.tensor(1., device=self.device),
                        constraint=constraints.positive)
        m_theta_param = pyro.param('loc_ability', torch.zeros(self.num_models, device=self.device))
        s_theta_param = pyro.param('scale_ability', torch.ones(self.num_models, device=self.device),
                            constraint=constraints.positive)
        m_b_param = pyro.param('loc_diff', torch.zeros(self.num_items, device=self.device))
        s_b_param = pyro.param('scale_diff', torch.ones(self.num_items, device=self.device),
                                constraint=constraints.positive)

        # sample statements
        pyro.sample('mu_b', dist.Normal(loc_mu_b_param, scale_mu_b_param))
        pyro.sample('u_b', dist.Gamma(alpha_b_param, beta_b_param))
        pyro.sample('mu_theta', dist.Normal(loc_mu_theta_param, scale_mu_theta_param))
        pyro.sample('u_theta', dist.Gamma(alpha_theta_param, beta_theta_param))
        
        with pyro.plate('thetas', self.num_models, device=self.device):
            pyro.sample('theta', dist.Normal(m_theta_param, s_theta_param))
        with pyro.plate('bs', self.num_items, device=self.device):
            pyro.sample('b', dist.Normal(m_b_param, s_b_param))

            
    def fit(self, models, items, responses, num_epochs):
        """Fit the IRT model with variational inference"""
        optim = Adam({'lr': 0.1})
        if self.priors == 'vague':
            svi = SVI(self.model_vague, self.guide_vague, optim, loss=Trace_ELBO())
        else:
            svi = SVI(self.model_hierarchical, self.guide_hierarchical, optim, loss=Trace_ELBO())
        
        pyro.clear_param_store()
        for j in range(num_epochs):
            loss = svi.step(models, items, responses)
            if j % 100 == 0 and self.verbose:
                print("[epoch %04d] loss: %.4f" % (j + 1, loss))

        print("[epoch %04d] loss: %.4f" % (j + 1, loss))
        values = ['loc_diff', 'scale_diff', 'loc_ability', 'scale_ability']

        
    def fit_MCMC(self, models, items, responses, num_epochs):
        """Fit the IRT model with MCMC"""
        sites = ['theta', 'b']
        nuts_kernel = NUTS(self.model_vague, adapt_step_size=True)
        hmc_posterior = MCMC(nuts_kernel, num_samples=1000, warmup_steps=100) \
            .run(models, items, responses) 
        theta_sum = self.summary(hmc_posterior, ['theta']).items() 
        b_sum = self.summary(hmc_posterior, ['b']).items() 
        print(theta_sum)
        print(b_sum)


    def summary(self, traces, sites):
        """Aggregate marginals for MCM"""
        marginal = EmpiricalMarginal(traces, sites)._get_samples_and_weights()[0].detach().cpu().numpy()
        print(marginal)
        site_stats = {}
        for i in range(marginal.shape[1]):
            site_name = sites[i]
            marginal_site = pd.DataFrame(marginal[:, i]).transpose()
            describe = partial(pd.Series.describe, percentiles=[.05, 0.25, 0.5, 0.75, 0.95])
            site_stats[site_name] = marginal_site.apply(describe, axis=1) \
                [["mean", "std", "5%", "25%", "50%", "75%", "95%"]]
        return site_stats
