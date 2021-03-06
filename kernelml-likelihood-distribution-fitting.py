import kernelml
from scipy import stats

def prior_sampler_custom(num_param):
        w1 = np.random.uniform(1,np.mean(X),size=(num_param,1000))
        w2 = np.random.normal(np.std(X),1,size=(num_param,1000))
        w3 = np.random.uniform(1,2,size=(num_param,1000))
        w = np.hstack((w1,w2,w3))
        return w

def liklihood_loss(x,y,w):
    hypothesis = x
    hypothesis[hypothesis<=0.00001] = 0.00001
    hypothesis[hypothesis>=0.99999] = 0.99999
    loss = -1*((1-y).T.dot(np.log(1-hypothesis)) + y.T.dot(np.log(hypothesis)))/len(y)
    return loss.flatten()[0]

def loss_function(x,y,w):
    alpha1,loc1,scale1 = w[0],w[1],w[2]
    rv = scale1*stats.norm(alpha1,loc1).pdf(x)
    loss = liklihood_loss(rv,y,w)
    return loss


vals, indx = np.histogram(train[['price']].values, normed=False,bins=30)
X = np.linspace(np.min(train[['price']].values),np.max(train[['price']].values),len(vals)) + np.diff(indx)
X = X.reshape(-1,1)
vals = vals.flatten()/np.max(vals)
vals = vals.reshape(-1,1)
model = kernelml.kernel_optimizer(X,vals,loss_function,num_param=6)
#change how the initial parameters are sampled
model.change_prior_sampler(prior_sampler_custom)
#change how many posterior samples are created for each parameter
model.default_random_simulation_params(random_sample_num=200)
model.adjust_optimizer(update_magnitude=10,analyze_n_parameters=50)
model.adjust_convergence_z_score(1.9)
model.kernel_optimize_(plot=True)   

errors = model.best_losses
params = model.best_parameters
params = np.array(params)
w = params[np.where(errors==np.min(errors))].T

mean1,std1,scale1 = w[0],w[1],w[2]

plt.stem(X, scale1*stats.norm.pdf(X,mean1,std1),'r', lw=5, alpha=0.6, label='normal pdf')
plt.plot(X,vals)
plt.show()
