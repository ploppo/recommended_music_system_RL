import pykeen
from typing import List
import torch
from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline
from pykeen.models import TransR
from pykeen.models import TransE
from pykeen.evaluation import evaluator
#


print('model Trans begin')
tf = TriplesFactory.from_path('triplets_medium.tsv')
training, testing = tf.split()
#choosing the model
model = TransR(triples_factory=tf, embedding_dim=10, relation_dim=10)
#model = TransE(triples_factory=tf, embedding_dim=10)
result = pipeline(
    training=training,
    testing=testing,
    model=model,
    # evaluator= a,
    epochs=1)
# result of the embedding
model = result.model
entity_representation_modules: List['pykeen.nn.Representation'] = model.entity_representations
relation_representation_modules: List['pykeen.nn.Representation'] = model.relation_representations
entity_embeddings: pykeen.nn.Embedding = entity_representation_modules[0]
relation_embeddings: pykeen.nn.Embedding = relation_representation_modules[0]
# entity and relation in tensor
entity_embedding_tensor: torch.FloatTensor = entity_embeddings()
relation_embedding_tensor: torch.FloatTensor = relation_embeddings()

result.save_to_directory('model_transE')

print('model Trans end')