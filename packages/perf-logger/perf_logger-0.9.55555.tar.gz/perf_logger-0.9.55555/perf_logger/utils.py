import numpy as np
filtr = lambda s: ''.join([_s for _s in s if _s in '0123456789.'])

def guess_value(l,name,):
    if name in l:
        v = l.split(name)[-1].split()[0]
        v = filtr(v)
        try:
            v = float(v)
            return v
        except:
            return None
def _parse_lines(lines):
    acc = []
    loss = []
    epoch = []
    batch = []

    for l in lines:
        acc += [guess_value(l,'acc')]
        loss += [guess_value(l,'loss')]
        epoch += [guess_value(l,'epoch')]
        batch += [guess_value(l,'batch')]   
    
    return {'epoch':epoch,'batch':batch,'acc':acc,'loss':loss}
def parse_log(log_file):
    lines = open(log_file).read().split('\n')   
    lines = [l.lower() for l in lines]
    train_lines = [l for l in lines if 'train' in l and 'loss' in l]
    val_lines = [l for l in lines if 'val' in l and 'loss' in l]
    
    test_lines = [l for l in lines if 'test' in l and 'loss' in l]
    
    train_stats = _parse_lines(train_lines)
    val_stats = _parse_lines(val_lines)
    test_stats = _parse_lines(test_lines)
    return train_stats,val_stats,test_stats
    
def average_by_epoch(stats):
    epochs = np.sort(list(set(stats['epoch'])))
    acc = np.array(stats['acc'])
    loss = np.array(stats['loss'])

    avg_acc = [np.mean(acc[np.array(stats['epoch'])==e]) for e in epochs]
    avg_loss = [np.mean(loss[np.array(stats['epoch'])==e]) for e in epochs]
    return avg_acc,avg_loss   
