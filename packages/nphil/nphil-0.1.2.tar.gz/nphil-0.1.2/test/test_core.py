import numpy as np
import nphil

def check(f):
    nodes = f.getNodes()

f = nphil.FGraph("moment", 0.5, 3.0, 0.5)
f.addRootNode("x", "+", "-0", 1.0, "e")
f.addRootNode("y", "+-", "+0", 1.0, "e")
f.addLayer("el|sr2", "+")
f.generate()

check(f)
print("Continue")
for node in f.getNodes():
    print(node.expr)
input('...')

n_samples = 10
n_vars = 2
n_features = len(f)
n_rand = 3
X = np.random.uniform(size=(n_samples, n_vars))
y = np.copy(X[:,1]+X[:,0]).reshape((-1,1))
X_out = np.zeros((n_samples, n_features))
C_out = np.zeros((n_features, n_rand))
C_out = np.zeros((n_rand, n_features))

print(X)
f.apply(X, X_out, n_samples)
print(X_out)

print(X)
X_out = np.zeros((n_samples, n_features))
f.applyAndCorrelate(
    X, y, X_out, C_out[1], n_samples, 1)
print(X_out)
print(C_out)


#for node in f.getNodes():
#    print(node.expr, node.is_root)

print(np.mean(X_out, axis=0))
#print(C_out)

#f.applyAndCorrelate(
#    X_out, C_out, X, y, n_samples, n_vars)
#print(X_out)
#print(X_out)
#print(C_out)

