import codecs
import sys

#分开learner和native

def split(data_dir, pos_dir, neg_dir):
    i = 0
    with codecs.open(data_dir, 'r') as f1:
        with codecs.open(pos_dir, 'w') as f2:
            with codecs.open(neg_dir, 'w') as f3:
                for line in f1.readlines():
                    try:
                        line = line.strip()
                        neg, pos = line.split('\t')
                        neg = neg.strip()
                        pos = pos.strip()
                        f2.write(pos + '\n')
                        f3.write(neg + '\n')
                    except:
                        i += 1
                        print(i, "lines are not right format")

if __name__ == "__main__":
    args = sys.argv
    data_dir = args[1]
    pos_dir = args[2]
    neg_dir = args[3]
    split(data_dir, pos_dir, neg_dir)



