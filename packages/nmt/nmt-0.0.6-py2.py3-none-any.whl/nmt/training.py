import torch
import numpy as np
import tqdm
from nmt.utils.postprocess import detokenize_sentences


def train(model, optimizer, train_loader, state, debug=False,disable_progress_bar=False):
    """ Trains an instance of a Seq2Seq pytorch model

    Inputs:
        model: an instance of Seq2Seq
        optimzer: torch.optimizer module
        train_loader: training set data loader
        state: latest state_dict for all the learnable model parameters
        debug:
    """
    epoch, n_epochs = state

    losses = []

    t = tqdm.tqdm(train_loader,disable=disable_progress_bar)

    # Set the self.training attribute in Seq2Seq module to True
    model.train()

    for batch in t:
        t.set_description("Epoch {:.0f}/{:.0f} (train={})".format(epoch, n_epochs, model.training))
        loss, _, _, _ = model.loss(batch)
        losses.append(loss.item())
        # Reset gradients
        optimizer.zero_grad()
        # Compute gradients
        loss.backward()
        optimizer.step()
        t.set_postfix(loss='{:05.3f}'.format(loss.item()), avg_loss='{:05.3f}'.format(np.mean(losses)))
        t.update()

    avg_loss = np.mean(losses)

    return model, optimizer, avg_loss

def evaluate(model, eval_loader, targ_index, scorer, debug=False,disable_progress_bar=False):

    losses = []

    t = tqdm.tqdm(eval_loader,disable=disable_progress_bar)
    model.eval()

    all_decoded_targets = []
    all_decoded_pred = []

    with torch.no_grad():
        for batch in t:
            t.set_description(" Evaluating... (train={})".format(model.training))
            loss, logits, labels, final_sentences = model.loss(batch)

            cur_batch_size = final_sentences.size()[0]
            # Convert sentences from idx to list of list of words
            decoded_targets = detokenize_sentences(
                labels.view(cur_batch_size, -1),
                targ_index.idx2word,
                output='token')

            decoded_pred = detokenize_sentences(
                final_sentences,
                targ_index.idx2word,
                output='token')

            all_decoded_targets.extend(decoded_targets)
            all_decoded_pred.extend(decoded_pred)

            losses.append(loss.item())
            t.set_postfix(avg_loss='{}'.format(np.mean(losses)))
            t.update()

    if debug:
        print("len of target: {}, len of pred: {}".format(len(all_decoded_targets), len(all_decoded_pred)))

    # Calculate BLEU score - [0-100]
    acc = scorer(all_decoded_targets, all_decoded_pred, weights=(1, 0, 0, 0)) * 100

    # Calculate bag of word accuracy
    # acc = scorer(
    #       decoded_targets,
    #        decoded_pred,
    #        output='mean',
    #        debug=debug)

    print("  End of evaluation : loss {:05.3f} , BLEU score {:03.5f}".format(np.mean(losses), acc))

    avg_loss = np.mean(losses)
    return avg_loss, acc

# TODO: Random Sample - translation pair to compare results
