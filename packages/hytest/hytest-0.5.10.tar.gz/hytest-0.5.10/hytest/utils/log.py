_b=' case_st_lable'
_a='green'
_Z='case_abort_list'
_Y='case_fail_list'
_X='case_pass_list'
_W='tag'
_V=' fail'
_U='folder_header'
_T='folder_body'
_S='%Y%m%d_%H%M%S'
_R='用例'
_Q='log'
_P='info error-info'
_O='utf8'
_N='case_teardown_fail'
_M='suite_teardown_fail'
_L='case_setup_fail'
_K='suite_setup_fail'
_J='case_abort'
_I='case_fail'
_H='case_pass'
_G='case_count'
_F='label'
_E='suite'
_D='class'
_C='\n'
_B='Traceback:\n'
_A='bright_red'
import logging,os,time
from logging.handlers import RotatingFileHandler
from rich.console import Console
from rich.theme import Theme
from hytest.product import version
os.makedirs(_Q,exist_ok=True)
logger=logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
logFile=os.path.join(_Q,'testresult.log')
handler=RotatingFileHandler(logFile,maxBytes=1024*1024*30,backupCount=2,encoding=_O)
handler.setLevel(logging.DEBUG)
formatter=logging.Formatter(fmt='%(message)s')
handler.setFormatter(formatter)
handler.doRollover()
logger.addHandler(handler)
console=Console(theme=Theme(inherit=False))
print=console.print
class LogLevel:level=0
class Stats:
	def testStart(self,_title='Test Report'):self.result={_G:0,_H:0,_I:0,_J:0,_K:0,_L:0,_M:0,_N:0,_X:[],_Y:[],_Z:[]};self.start_time=time.time()
	def testEnd(self):self.end_time=time.time();self.test_duration=self.end_time-self.start_time
	def enter_case(self,caseId,name,case_className):self.result[_G]+=1
	def case_pass(self,caseId,name):self.result[_H]+=1;self.result[_X].append(caseId)
	def case_fail(self,caseId,name,e,stacktrace):self.result[_I]+=1;self.result[_Y].append(caseId)
	def case_abort(self,caseId,name,e,stacktrace):self.result[_J]+=1;self.result[_Z].append(caseId)
	def setup_fail(self,name,utype,e,stacktrace):
		if utype==_E:self.result[_K]+=1
		else:self.result[_L]+=1
	def teardown_fail(self,name,utype,e,stacktrace):
		if utype==_E:self.result[_M]+=1
		else:self.result[_N]+=1
stats=Stats()
class ConsoleLogger:
	def testEnd(self):A='white';ret=stats.result;print(f"\n\n  ========= 测试耗时 : {stats.test_duration:.3f} 秒 =========\n");print(f"\n  用例数量 : {ret[_G]}");print(f"\n  通过 : {ret[_H]}",style=_a);num=ret[_I];style=A if num==0 else _A;print(f"\n  失败 : {num}",style=style);num=ret[_J];style=A if num==0 else _A;print(f"\n  异常 : {num}",style=style);num=ret[_K];style=A if num==0 else _A;print(f"\n  套件初始化失败 : {num}",style=style);num=ret[_M];style=A if num==0 else _A;print(f"\n  套件清除  失败 : {num}",style=style);num=ret[_L];style=A if num==0 else _A;print(f"\n  用例初始化失败 : {num}",style=style);num=ret[_N];style=A if num==0 else _A;print(f"\n  用例清除  失败 : {num}",style=style)
	def enter_suite(self,name,suitetype):
		if suitetype=='file':print(f"\n\n>>> {name}",style='bold bright_black')
	def enter_case(self,caseId,name,case_className):print(f"\n* {name}",style='bright_white')
	def case_steps(self,name):...
	def case_pass(self,caseId,name):print('                          PASS',style=_a)
	def case_fail(self,caseId,name,e,stacktrace):print(f"                          FAIL\n{e}",style=_A)
	def case_abort(self,caseId,name,e,stacktrace):print(f"                          ABORT\n{e}",style='magenta')
	def case_check_point(self,msg):...
	def setup(self,name,utype):...
	def teardown(self,name,utype):...
	def setup_fail(self,name,utype,e,stacktrace):utype='套件'if utype==_E else _R;print(f"\n{utype} 初始化失败 | {name} | {e}",style=_A)
	def teardown_fail(self,name,utype,e,stacktrace):utype='套件'if utype==_E else _R;print(f"\n{utype} 清除失败 | {name} | {e}",style=_A)
	def debug(self,msg):
		if LogLevel.level>0:print(f"{msg}")
	def criticalInfo(self,msg):print(f"{msg}",style=_A)
class TextLogger:
	def testStart(self,_title=''):startTime=time.strftime(_S,time.localtime(stats.start_time));logger.info(f"\n\n  ========= 测试开始 : {startTime} =========\n")
	def testEnd(self):endTime=time.strftime(_S,time.localtime(stats.end_time));logger.info(f"\n\n  ========= 测试结束 : {endTime} =========\n");logger.info(f"\n  耗时    : {stats.end_time-stats.start_time:.3f} 秒\n");ret=stats.result;logger.info(f"\n  用例数量 : {ret[_G]}");logger.info(f"\n  通过 : {ret[_H]}");logger.info(f"\n  失败 : {ret[_I]}");logger.info(f"\n  异常 : {ret[_J]}");logger.info(f"\n  套件初始化失败 : {ret[_K]}");logger.info(f"\n  套件清除  失败 : {ret[_M]}");logger.info(f"\n  用例初始化失败 : {ret[_L]}");logger.info(f"\n  用例清除  失败 : {ret[_N]}")
	def enter_suite(self,name,suitetype):logger.info(f"\n\n>>> {name}")
	def enter_case(self,caseId,name,case_className):logger.info(f"\n* {name}")
	def case_steps(self,name):logger.info(f"\n  [ case execution steps ]")
	def case_pass(self,caseId,name):logger.info('  PASS ')
	def case_fail(self,caseId,name,e,stacktrace):stacktrace=_B+stacktrace.split(_C,3)[3];logger.info(f"  FAIL   {e} \n{stacktrace}")
	def case_abort(self,caseId,name,e,stacktrace):stacktrace=_B+stacktrace.split(_C,3)[3];logger.info(f"  ABORT   {e} \n{stacktrace}")
	def case_check_point(self,msg):logger.info(f"\n-- check {msg}")
	def setup(self,name,utype):logger.info(f"\n[ {utype} setup ] {name}")
	def teardown(self,name,utype):logger.info(f"\n[ {utype} teardown ] {name}")
	def setup_fail(self,name,utype,e,stacktrace):stacktrace=_B+stacktrace.split(_C,3)[3];logger.info(f"{utype} setup fail | {e} \n{stacktrace}")
	def teardown_fail(self,name,utype,e,stacktrace):stacktrace=_B+stacktrace.split(_C,3)[3];logger.info(f"{utype} teardown fail | {e} \n{stacktrace}")
	def info(self,msg):logger.info(msg)
	def debug(self,msg):
		if LogLevel.level>0:logger.debug(msg)
	def step(self,stepNo,desc):logger.info(f"\n-- 第 {stepNo} 步 -- {desc} \n")
	def checkpoint_pass(self,desc):logger.info(f"\n** 检查点 **  {desc} ---->  通过\n")
	def checkpoint_fail(self,desc):logger.info(f"\n** 检查点 **  {desc} ---->  !! 不通过!!\n")
	def criticalInfo(self,msg):logger.info(f"!!! {msg} !!!")
from dominate.tags import *
from dominate.util import raw
from dominate import document
class HtmlLogger:
	def testStart(self,_title=''):
		B=None;A='menu-item'
		with open(os.path.join(os.path.dirname(__file__),'report.css'),encoding=_O)as f:_css_style=f.read()
		with open(os.path.join(os.path.dirname(__file__),'report.js'),encoding=_O)as f:_js=f.read()
		self.doc=document(title=f"测试报告");self.doc.head.add(meta(charset='UTF-8'),style(raw(_css_style)),script(raw(_js),type='text/javascript'));self.main=self.doc.body.add(div(_class='main_section'));self.main.add(h1(f"测试报告 - hytest v{version}",style='font-family: auto'));_,self.stats=self.main.add(h3(f"统计结果"),table(_class='result_stats'));_,self.logDiv=self.main.add(div(h3('执行日志',style='display:inline'),style='margin-top:2em'),div(_class='exec_log'));self.ev=div(div('∧',_class=A,onclick='previous_error()',title='上一个错误'),div('∨',_class=A,onclick='next_error()',title='下一个错误'),_class='error_jumper');self.main.add(div(div('页首',_class=A,onclick='document.querySelector("body").scrollIntoView()'),div('教程',_class=A,onclick='window.open("http://www.python3.vip/tut/auto/hytest/01", "_blank"); '),div('精简',_class=A,id='display_mode',onclick='toggle_folder_all_cases()'),self.ev,id='float_menu'));self.curEle=self.main;self.curSuiteEle=B;self.curCaseEle=B;self.curCaseLableEle=B;self.curSetupEle=B;self.curTeardownEle=B;self.suitepath2element={}
	def testEnd(self):
		B='%Y%m%d %H:%M:%S';A='color:red';execStartTime=time.strftime(B,time.localtime(stats.start_time));execEndTime=time.strftime(B,time.localtime(stats.end_time));ret=stats.result;errorNum=0;trs=[];trs.append(tr(td('开始时间'),td(f"{execStartTime}")));trs.append(tr(td('结束时间'),td(f"{execEndTime}")));trs.append(tr(td('耗时'),td(f"{stats.test_duration:.3f} 秒")));trs.append(tr(td('用例数量'),td(f"{ret[_G]}")));trs.append(tr(td('通过'),td(f"{ret[_H]}")));num=ret[_I];style=''if num==0 else A;trs.append(tr(td('失败'),td(f"{num}",style=style)));errorNum+=num;num=ret[_J];style=''if num==0 else A;trs.append(tr(td('异常'),td(f"{num}",style=style)));errorNum+=num;num=ret[_K];style=''if num==0 else A;trs.append(tr(td('套件初始化失败'),td(f"{num}",style=style)));errorNum+=num;num=ret[_M];style=''if num==0 else A;trs.append(tr(td('套件清除失败'),td(f"{num}",style=style)));errorNum+=num;num=ret[_L];style=''if num==0 else A;trs.append(tr(td('用例初始化失败'),td(f"{num}",style=style)));errorNum+=num;num=ret[_N];style=''if num==0 else A;trs.append(tr(td('用例清除失败'),td(f"{num}",style=style)));errorNum+=num;self.ev['display']='none'if errorNum==0 else'block';self.stats.add(tbody(*trs));htmlcontent=self.doc.render();timestamp=time.strftime(_S,time.localtime(stats.start_time));reportFile=os.path.join(_Q,f"log_{timestamp}.html")
		with open(reportFile,'w',encoding=_O)as f:f.write(htmlcontent)
		try:os.startfile(reportFile)
		except:
			try:os.system(f"open {reportFile}")
			except:...
	def enter_suite(self,name,suitetype):_class='suite_'+suitetype;enterInfo='进入目录'if suitetype=='dir'else'进入文件';self.curEle=self.logDiv.add(div(div(span(enterInfo,_class=_F),span(name)),_class=_class,id=f"{_class} {name}"));self.curSuiteEle=self.curEle;self.curSuiteFilePath=name;self.suitepath2element[name]=self.curEle
	def enter_case(self,caseId,name,case_className):self.curCaseLableEle=span(_R,_class='label caselabel');self.curCaseBodyEle=div(span(f"{self.curSuiteFilePath}::{case_className}",_class='case_class_path'),_class=_T);self.curCaseEle=self.curSuiteEle.add(div(div(self.curCaseLableEle,span(name,_class='casename'),_class=_U),self.curCaseBodyEle,_class='case',id=f"case_{caseId:08}"));self.curEle=self.curCaseBodyEle
	def case_steps(self,name):ele=div(span('测试步骤',_class=_F),_class='test_steps',id='test_steps '+name);self.curEle=self.curCaseBodyEle.add(ele)
	def case_pass(self,caseId,name):self.curCaseEle[_D]+=' pass';self.curCaseLableEle+=' PASS'
	def case_fail(self,caseId,name,e,stacktrace):self.curCaseEle[_D]+=_V;self.curCaseLableEle+=' FAIL';stacktrace=_B+stacktrace.split(_C,3)[3];self.curEle+=div(f"{e} \n{stacktrace}",_class=_P)
	def case_abort(self,caseId,name,e,stacktrace):self.curCaseEle[_D]+=' abort';self.curCaseLableEle+=' ABORT';stacktrace=_B+stacktrace.split(_C,3)[3];self.curEle+=div(f"{e} \n{stacktrace}",_class=_P)
	def case_check_point(self,msg):0
	def setup(self,name,utype):
		_class=f"{utype}_setup setup"
		if utype==_E:stHeaderEle=div(span('套件初始化',_class=_F),span(name),_class=_U);stBodyEle=self.curEle=div(_class=_T);self.curSetupEle=div(stHeaderEle,stBodyEle,_class=_class,id=f"{_class} {name}");self.curSuiteEle.add(self.curSetupEle)
		else:self.curSetupEle=self.curEle=div(span('用例初始化',_class=_F),_class=_class,id=f"{_class} {name}");self.curCaseBodyEle.add(self.curSetupEle);self.curEle[_D]+=_b
	def teardown(self,name,utype):
		_class=f"{utype}_teardown teardown"
		if utype==_E:stHeaderEle=div(span('套件清除',_class=_F),span(name),_class=_U);stBodyEle=self.curEle=div(_class=_T);self.curTeardownEle=div(stHeaderEle,stBodyEle,_class=_class,id=f"{_class} {name}");self.curSuiteEle.add(self.curTeardownEle)
		else:self.curTeardownEle=self.curEle=div(span('用例清除',_class=_F),_class=_class,id=f"{_class} {name}");self.curCaseBodyEle.add(self.curTeardownEle);self.curEle[_D]+=_b
	def setup_fail(self,name,utype,e,stacktrace):self.curSetupEle[_D]+=_V;stacktrace=_B+stacktrace.split(_C,3)[3];self.curEle+=div(f"{utype} setup fail | {e} \n{stacktrace}",_class=_P)
	def teardown_fail(self,name,utype,e,stacktrace):self.curTeardownEle[_D]+=_V;stacktrace=_B+stacktrace.split(_C,3)[3];self.curEle+=div(f"{utype} teardown fail | {e} \n{stacktrace}",_class=_P)
	def info(self,msg):self.curEle+=div(msg,_class='info')
	def step(self,stepNo,desc):self.curEle+=div(span(f"第 {stepNo} 步",_class=_W),span(desc),_class='case_step')
	def checkpoint_pass(self,desc):self.curEle+=div(span(f"检查点 PASS",_class=_W),span(desc),_class='checkpoint_pass')
	def checkpoint_fail(self,desc):self.curEle+=div(span(f"检查点 FAIL",_class=_W),span(desc),_class='checkpoint_fail')
from .signal import signal
signal.register([stats,ConsoleLogger(),TextLogger(),HtmlLogger()])