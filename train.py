from parlai.scripts.train_model import TrainModel
TrainModel.main(
# similar to before
multitask_weights = [2, 6, 3, 3],
task='nsfwdata',
model='transformer/generator',
model_file='~/ParlAI/blendernsfw',

# initialize with a pretrained model
#init_model='zoo:tutorial_transformer_generator/model',
#init_model='finetuned/model',

# arguments we get from the pretrained model.
# Unfortunately, these must be looked up separately for each model.
n_heads=16, n_layers=8, n_positions=512, text_truncate=512,
label_truncate=128, ffn_size=2048, embedding_size=512,
activation='gelu', variant='xlm',
dict_lower=True, dict_tokenizer='bpe',
#dict_file='zoo:tutorial_transformer_generator/model.dict',
#dict_file = 'finetuned/model.dict',
learn_positional_embeddings=True,

# some training arguments, specific to this fine-tuning
# use a small learning rate with ADAM optimizer
lr=1e-5, optimizer='adam',
warmup_updates=-1,
# early stopping on perplexity
validation_metric='ppl',
# train at most steps, and validate every 0.25 epochs
eps=9, validation_every_n_epochs=0.25,


batchsize=8, fp16=True, fp16_impl='mem_efficient',

# speeds up validation
skip_generation=True,

# helps us cram more examples into our gpu at a time
dynamic_batching='full',

)