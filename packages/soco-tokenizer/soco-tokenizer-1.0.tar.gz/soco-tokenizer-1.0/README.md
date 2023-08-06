# Tokenizer
Tokenizer different language fast.


## Build a package
    python setup.py bdist_wheel
    twine upload dist/*

## Use Locally
    x1 = '<a>刘强东是一个著名企业家。</a> 他创建了京东。'
    t = EncoderLoader.load_tokenizer('bert-base-chinese-zh_v4-10K')
    print(t.tokenize(x1, mode='char'))
    print(t.tokenize(x1, mode='word'))
    print(t.tokenize(x1, mode='all'))