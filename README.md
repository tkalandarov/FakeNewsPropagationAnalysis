# Fake News Propagation Analysis and Detection Project
CIS 4930 Social Networks Analysis (Fall 2024)

## Overview

This repository consolidates two projects focused on understanding and detecting fake news propagation in social networks. By leveraging advanced graph-based techniques and machine learning models, we explore the dynamics of misinformation spread and develop tools to classify news articles as real or fake based on network behaviors and emotional content.

## Objectives

- Analyze fake news propagation through **user-to-user** and **news-centered** graphs.
- Validate hypotheses on the spread of fake news using data-driven experiments.
- Train **Graph Neural Network (GNN)** models (e.g., **GraphSAGE**, **Graph Attention Networks**) for fake news detection.
- Extract insights on the emotional and structural aspects of fake news spread.

## Dataset

We used the [FakeNewsNet Dataset](https://www.kaggle.com/datasets/mdepak/fakenewsnet/discussion/166540), which includes:

1. **News Articles**:
   - 91 real and 91 fake news articles with full text, headlines, publisher details, and images.
2. **User-News Interactions**:
   - 22,780 samples of users sharing news articles.
3. **User-User Interactions**:
   - 634,750 directed edges representing follower-followee relationships.
4. **User Profiles**:
   - Encoded profiles of 15,258 users, providing attributes for susceptibility and connectivity.

## Key Theories

1. **Cluster Susceptibility**:
   - Users with high susceptibility to fake news cluster together and play a pivotal role in its spread.
2. **Emotion and Content**:
   - Fake news articles often exhibit higher negative emotional tones (e.g., fear, anger) compared to real news.
3. **Propagation Scale**:
   - Fake news tends to spread faster within tightly connected networks.
4. **Graph Variability**:
   - Structural variations in graphs (e.g., number of hops, inclusion/exclusion of central nodes) influence detection performance.


## Methodology

### Graph Construction

1. **User-to-User Graphs**:
   - Nodes: Users in the network.
   - Edges: Directed edges between follower-followee pairs.

2. **News-Centered Graphs**:
   - Nodes: News articles, users who share the news, and their followers.
   - Edges:
     - News-to-User (sharing news).
     - User-to-Follower (propagation within the network).

### Feature Engineering

- **Node Features**:
  - User: Follower and followee counts, fake/real news sharing susceptibility, emotional tone of shared posts.
  - News: Emotional intensity (anger, fear, joy, neutrality, etc.).
- **Edge Features**:
  - Interaction frequencies, directionality, and weights.
- **Graph Metrics**:
  - Modularity, clustering coefficients, graph diameter, and node centrality.

### Machine Learning Models

1. **GraphSAGE**:
   - Generates node embeddings by aggregating neighborhood information.
   - Best performance achieved with:
     - Hidden layers: 1
     - Hidden layer size: 2048
     - Learning rate: 0.01
     - Epochs: 200
     - Loss: Negative Log Likelihood

2. **Graph Attention Networks (GAT)**:
   - Improved attention mechanisms for better feature aggregation.


## Results

- **Performance Metrics**:
  - Best accuracy: **85.45%**
  - F1-Score: **0.8519**
- **Graph Variations**:
  - Undirected graphs excluding central news nodes performed best.
  - Optimal hop size: **3** (maximum node distance from the central news node).
- **Feature Insights**:
  - Emotional tones (anger, fear) significantly enhanced detection accuracy.

## Tools and Frameworks

- **PyTorch**:
  - Implemented GNNs (GraphSAGE, GAT) and custom training workflows.
- **Hugging Face**:
  - Used pre-trained emotion models (e.g., DistilRoBERTa) for content analysis.
- **Gephi**:
  - Visualized graph structures for exploratory analysis.
- **Python Libraries**:
  - `networkx`: Graph construction and manipulation.
  - `pandas` and `numpy`: Data preprocessing and analysis.

## Contributions

- **Timur Kalandarov**:
  - Developed graph construction and embedding logic.
  - Collaborated on optimizing GNN implementation and feature engineering.
- **Zaima Zarnaz**:
  - Extracted user features and trained models with extensive experimentation.
- **Muhammad Zain Ali**:
  - Created user-user graphs and optimized GAT algorithms.
- **Ethan Tracy**:
  - Built news-to-user graphs and managed server configurations for model training.

## Future Work

- Integrate real-time social media data for enhanced model generalization.
- Explore larger datasets and advanced GNN architectures (e.g., Graph Transformers).
- Implement temporal analysis for better understanding of misinformation dynamics.

## References

1. Sormeily et al., "MEFaND: A Multimodel Framework for Early Fake News Detection," IEEE, 2024.
2. Chalehchaleh et al., "BRaG: A Hybrid Multi-Feature Framework for Fake News Detection," Social Network Analysis, 2024.
3. Hartmann, "Emotion English DistilRoBERTa Base," Hugging Face, 2023.
