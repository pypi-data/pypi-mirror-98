import argparse,re,os
from os.path import isdir
from hytest.utils.log import LogLevel
from .utils.runner import Collector,Runner
from .product import version

from .product import version



def printLogo():    
    print(f'''           
    *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *     
    *       hytest {version}             www.python3.vip   *
    *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    '''
    )




def tagExpressionGen(argstr):
    tagRules = []
    for part in argstr:
        # 有单引号，是表达式
        if "'" in part:
            rule = re.sub(r"'.+?'", lambda m :f'tagmatch({m.group(0)})' , part)
            tagRules.append(f'({rule})')
        # 是简单标签名
        else:
            rule = f"tagmatch('{part}')"
            tagRules.append(f'{rule}')
    return ' or '.join(tagRules)

def run() :
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f'hytest v{version}',help="显示版本号" )
    parser.add_argument('--new',  metavar='project_dir', help="创建新项目目录" )
    parser.add_argument("case_dir", help="用例根目录", nargs='?', default='cases')
    parser.add_argument("-L", "--loglevel", metavar='Level_Number', type=int, help="日志级别  0:低 - 1:高", default=0)

    parser.add_argument("--test", metavar='Case_Name', action='append', help="用例名过滤，支持通配符", default=[])
    parser.add_argument("--suite", metavar='Suite_Name', action='append', help="套件名过滤，支持通配符", default=[])
    parser.add_argument("--tag", metavar='Tag_Expression', action='append', help="标签名过滤，支持通配符", default=[])
    parser.add_argument("--tagnot", metavar='Tag_Expression', action='append', help="标签名过滤，支持通配符", default=[])
    parser.add_argument("-A", "--argfile", metavar='Argument_File', help="参数文件", type=argparse.FileType('r', encoding='utf8'))


    args = parser.parse_args()
    # 有参数放在文件中
    if args.argfile:
        fileArgs = [para for para in args.argfile.read().replace('\n',' ').split() if para]
        print(fileArgs)
        args = parser.parse_args(fileArgs,args)

    # 创建项目目录
    if args.new:
        projDir =  args.new
        if os.path.exists(projDir):
            print(f'{projDir} already exists！')
            exit(2)
        os.makedirs(f'{projDir}/cases')
        with open(f'{projDir}/cases/case1.py','w',encoding='utf8') as f:
            f.write('''class c1:
    name = '用例名称 - 0001'

    # 测试用例步骤
    def teststeps(self):...''')

        exit()


    LogLevel.level = args.loglevel
    # print('loglevel',LogLevel.level)

    if not os.path.exists(args.case_dir) or not os.path.isdir(args.case_dir):
        print(f'命令行参数 case_dir 错误:  {args.case_dir}')
        exit(2)

    # --tag "'冒烟测试' and 'UITest' or (not '快速' and 'fast')" --tag 白月 --tag 黑羽


    tag_include_expr = tagExpressionGen(args.tag)
    tag_exclude_expr = tagExpressionGen(args.tagnot)

    # print(tag_include_expr)
    # print(tag_exclude_expr)

    printLogo()

    Collector.run(
        casedir=args.case_dir,
        suitename_filters=args.suite,
        casename_filters=args.test,
        tag_include_expr=tag_include_expr,
        tag_exclude_expr=tag_exclude_expr,
        )
    Runner.run()

if __name__ == '__main__':
    run()