from cleantxt import text
from tqdm import tqdm
import argparse
import os


def rule(s):
    try:
        k, v = map(str, s.split(','))
        return k, v
    except:
        raise argparse.ArgumentTypeError("Escape Rule must be key,value ")


def main():
    parser = argparse.ArgumentParser(
        prog="cleantxt cleaning text from noise commande line interface",
        description="Arguments for cleantxt to clean document from noise (cleantxt)",
        usage="""  cleantxt --doc=[path_to_doc] 
                  --out=[path_out_file]
                  --f=[0] 
                  --t=[100] 
                  --do_lower=True
                  --white_space=True 
                  --punctuation=True 
                  --duplicated_chars=True
                  --alpha_num=True 
                  --accent=True 
                  --escape key,value ə,a œ,oe""",
        allow_abbrev=False
    )

    parser.add_argument(
        "--doc",
        type=str,
        help="path of document to clean it",
        required=True
    )

    parser.add_argument(
        "--out",
        default="out.txt",
        type=str,
        help="path of clean document (default out.txt)",
        required=False
    )

    parser.add_argument(
        "--f",
        default=0,
        type=int,
        help="index of starting document (default 0)",
        required=False
    )

    parser.add_argument(
        "--t",
        default=None,
        type=int,
        help="index of end of document (default None) meaning the end of document",
        required=False
    )

    parser.add_argument(
        "--escape",
        default=False,
        type=rule,
        help="Custom escape rules list with tuple k,v space k1,v1 ...",
        required=False,
        nargs='+'
    )

    parser.add_argument(
        "--do_lower",
        default=True,
        type=bool,
        help="Lower case all text (default True)",
        required=False
    )

    parser.add_argument(
        "--white_space",
        default=True,
        type=bool,
        help="Escape more then one spaces (default True)",
        required=False
    )

    parser.add_argument(
        "--punctuation",
        default=False,
        type=bool,
        help="Escape punctuation (default False)",
        required=False
    )

    parser.add_argument(
        "--duplicated_chars",
        default=False,
        type=bool,
        help="Escape duplicated chars more then two time (default False)",
        required=False
    )

    parser.add_argument(
        "--alpha_num",
        default=True,
        type=bool,
        help="Escape non alpha numeric chars (default True)",
        required=False
    )

    parser.add_argument(
        "--accent",
        default=False,
        type=bool,
        help="Escape accents (default False)",
        required=False
    )

    args = parser.parse_args()

    if args.t:
        if args.f > args.t:
            raise Exception("--f must be lower then --t")

    if not os.path.exists(args.doc):
        raise FileNotFoundError(
            'document not exist : {}'.format(args.doc)
        )

    if os.path.splitext(args.doc)[1] not in ['.txt', '.tab']:
        raise Exception(
            'file not accepted please chose (txt) or (tab) file'
        )

    file = open(args.doc, mode='r', encoding='utf8')
    data = file.readlines()

    if args.t:
        data_process = data[args.f:args.t]
    else:
        data_process = data

    if args.escape:
        escape = args.escape
    else:
        escape = None

    with open(args.out, mode='w+', encoding='utf8') as out_file:

        for x in tqdm(data_process, desc='clean document with cleantxt cli'):
            out_file.write(
                text.clean_text(
                    x,
                    witespace=args.white_space,
                    punctuation=args.punctuation,
                    duplicated=args.duplicated_chars,
                    alphnum=args.alpha_num,
                    accent=args.accent,
                    others=escape
                ) + '\n'
            )


if __name__ == '__main__':
    main()
