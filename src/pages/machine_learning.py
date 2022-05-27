import streamlit as st
from sklearn.datasets import make_blobs, make_circles
import matplotlib.pyplot as plt

import numpy as np

from .utils import create_font, plot_svc_decision_function


def app():
    create_font(30, '(Traditional) Machine Learning and Deep Learning')
    st.write(r'''
        - *What's the difference?*
        - Before Deep Learning: manual feature engineering, need expert knowledge about topic: how well do the features encode data patterns?
        - Deep Learning exposes patterns in the data/learns the patterns with automatic feature extraction (-> un-explainibility issue in Deep Learning) 

        
        - *Supervised Machine Learning*:
            - requires data with ground truth (labels)
            - models are specifically being corrected/guided during learning process
            - e.g. Decision Trees/Random Forests, Support Vector Machines, Convolutional Neural Networks 
        - *Unsupervised Machine Learning*:
            - no need for labeled data
            - model identify/derive patterns on their own
            - e.g. Clustering, AutoEncoders (input reconstruction)
            
    ''')
    with st.expander('Support Vector Machines'):
        st.write(r'''
            - Powerful supervised algorithms for regression or classification
            - Tries to find a hyperplane (e.g. a line in a 2D space) that divides data into separate classes
            - Intuition: Not just any hyperplane (line), but the one that maximizes the margin between the two classes
            to account for unseen data = "optimal model"
            - works well with few samples and is robust to class imbalance (unlike most deep learning models)
        ''')
        support_vector_machines()


def support_vector_machines():

    # plot data
    X, y = make_blobs(n_samples=50, centers=2, random_state=0, cluster_std=0.60)
    fig, ax = plt.subplots(1)
    ax.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='winter')
    checkbox = st.checkbox('Show possible dividing lines')
    if checkbox:
        xfit = np.linspace(-1, 3.5)
        for m, b in [(1, 0.65), (0.5, 1.6), (-0.2, 2.9)]:
            ax.plot(xfit, m * xfit + b, '-k')

            ax.set_xlim(-1, 3.5)
    st.pyplot(fig)

    with st.echo('Fit an SVM classifier in 2 lines of code'):
        # from sklearn.datasets import make_blobs
        # X, y = make_blobs(n_samples=50, centers=2, random_state=0, cluster_std=0.60)
        from sklearn.svm import SVC
        model = SVC(kernel='linear', C=1E10)
        model.fit(X, y)

    st.markdown('''
        ---
        ##
    ''')

    fig, ax = plt.subplots(1)
    ax.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
    plot_svc_decision_function(model)
    # fig.title('Plotting the optimal decision hyperplane')
    st.pyplot(fig)

    st.markdown('''
        ---
        ##
    ''')

    create_font(20, 'What if data is not linearly separable?')
    X, y = make_circles(100, factor=.1, noise=.1)
    fig, ax = plt.subplots(1)

    clf = SVC(kernel='linear').fit(X, y)
    plt.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')
    plot_svc_decision_function(clf, plot_support=False)
    st.pyplot(fig)

    st.write(r'''
        - Data is not linearly separable, it is impossible to find a fitting decision boundary
        - Solution: project data into a higher dimension so that a linear separation is possible:
    ''')
    st.markdown('''
        ---
        ##
    ''')

    plot_3D(elev=30, azim=30, X=X, y=y)
    st.write(r'''
        - The function to transform the coordinate space into a higher dimension needs to be learned
        - This process is built in to the SVM fitting function in python libraries, but requires careful tuning
        to the dataset
        - SVMs are usually faster, more efficient and require less memory than deep neural networks
        - They are are often more powerful than simpler machine learning models (linear models, decision trees) but less powerful than 
        deep networks 
        - Good alternative for classification problems with small, imbalanced datasets
    ''')

def plot_3D(X, y, elev=30, azim=30, ):
    r = np.exp(-(X ** 2).sum(1))
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter3D(X[:, 0], X[:, 1], r, c=y, s=50, cmap='autumn')
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('r')
    st.pyplot(fig)
    # interact(plot_3D, elev=[-90, 90], azip=(-180, 180), X=fixed(X), y=fixed(y));


