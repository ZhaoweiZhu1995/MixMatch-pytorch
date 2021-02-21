from __future__ import print_function, absolute_import
import torch
__all__ = ['accuracy']

def accuracy(output, target, topk=(1,), per_class = False):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    if per_class:
        # per class accuracy, only top1
        num_classes = output.size(1)
        res_per_class = torch.zeros(num_classes)
        rec_num = torch.zeros(num_classes)
        for class_i in range(num_classes):
            correct_class = correct * (target.view(1, -1) == class_i).expand_as(pred)
            correct_k = correct_class[0].view(-1).float().sum(0)
            rec_num[class_i] = torch.sum(target == class_i)
            res_per_class[class_i] = (correct_k.mul_(100.0 / rec_num[class_i]))
        return res_per_class, rec_num
    else:
        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res

