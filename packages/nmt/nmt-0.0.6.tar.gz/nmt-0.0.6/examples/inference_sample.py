"""This is testing the new Translator module"""

from nmt.inference import Translator

# Define location of model binary
dir_path = '/home/user/nmt/dev/export_model/202101211801_epoch_2_bz_32'
model_name = 'epoch_1_val_loss_5.244.pt'

# Load Seq2seq model
my_translator = Translator(dir_path=dir_path,
                           model_name=model_name)
my_translator.load_all_pretrained_components(gpu_enabled=False, debug=False)

# Translate !
spanish_sentences = ['Buenas noches!', '¡Que gusto de verlo!', 'Hasta luego.']
output_df = my_translator.corpus_translate(spanish_sentences)
print(output_df)


one_sentence = 'Que tengas un buen día '
my_translator.sentence_translate(one_sentence, display=True)
