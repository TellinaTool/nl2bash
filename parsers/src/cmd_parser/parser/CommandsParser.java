// Generated from Commands.g4 by ANTLR 4.5.3
package cmd_parser.parser;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class CommandsParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.5.3", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, T__21=22, T__22=23, T__23=24, 
		T__24=25, T__25=26, T__26=27, T__27=28, T__28=29, T__29=30, T__30=31, 
		T__31=32, T__32=33, T__33=34, T__34=35, T__35=36, T__36=37, T__37=38, 
		T__38=39, T__39=40, T__40=41, T__41=42, T__42=43, T__43=44, T__44=45, 
		T__45=46, T__46=47, T__47=48, T__48=49, T__49=50, T__50=51, T__51=52, 
		T__52=53, T__53=54, T__54=55, T__55=56, T__56=57, T__57=58, T__58=59, 
		T__59=60, T__60=61, T__61=62, T__62=63, T__63=64, T__64=65, T__65=66, 
		T__66=67, T__67=68, T__68=69, T__69=70, T__70=71, T__71=72, T__72=73, 
		T__73=74, T__74=75, T__75=76, T__76=77, T__77=78, T__78=79, T__79=80, 
		T__80=81, T__81=82, T__82=83, T__83=84, T__84=85, T__85=86, T__86=87, 
		T__87=88, T__88=89, T__89=90, T__90=91, T__91=92, T__92=93, T__93=94, 
		T__94=95, T__95=96, T__96=97, T__97=98, T__98=99, T__99=100, T__100=101, 
		T__101=102, T__102=103, T__103=104, T__104=105, T__105=106, T__106=107, 
		T__107=108, T__108=109, T__109=110, T__110=111, T__111=112, T__112=113, 
		T__113=114, T__114=115, T__115=116, T__116=117, T__117=118, T__118=119, 
		T__119=120, T__120=121, T__121=122, T__122=123, T__123=124, T__124=125, 
		T__125=126, T__126=127, T__127=128, T__128=129, T__129=130, T__130=131, 
		T__131=132, T__132=133, T__133=134, T__134=135, T__135=136, T__136=137, 
		T__137=138, T__138=139, T__139=140, T__140=141, T__141=142, T__142=143, 
		T__143=144, T__144=145, T__145=146, T__146=147, T__147=148, T__148=149, 
		T__149=150, T__150=151, T__151=152, T__152=153, T__153=154, T__154=155, 
		T__155=156, T__156=157, T__157=158, T__158=159, T__159=160, T__160=161, 
		T__161=162, T__162=163, T__163=164, T__164=165, T__165=166, T__166=167, 
		T__167=168, T__168=169, T__169=170, T__170=171, T__171=172, T__172=173, 
		T__173=174, T__174=175, T__175=176, T__176=177, T__177=178, STRING=179, 
		WS=180;
	public static final int
		RULE_command = 0, RULE_tar_op47 = 1, RULE_unzip_op2 = 2, RULE_grep_op15 = 3, 
		RULE_ls_op21 = 4, RULE_cat_op3 = 5, RULE_sort_op2 = 6, RULE_unzip_op18 = 7, 
		RULE_ls_op28 = 8, RULE_zip_op26 = 9, RULE_sort_op5 = 10, RULE_tail_op4 = 11, 
		RULE_find_op15 = 12, RULE_xargs_op10 = 13, RULE_find_op51 = 14, RULE_zip_op16 = 15, 
		RULE_xargs_op9 = 16, RULE_find_op38 = 17, RULE_sort_op15 = 18, RULE_ls_op12 = 19, 
		RULE_chmod_op1 = 20, RULE_comm_op2 = 21, RULE_egrep_op0 = 22, RULE_rm_op6 = 23, 
		RULE_zip_op9 = 24, RULE_zip_op12 = 25, RULE_chmod_op5 = 26, RULE_egrep_op22 = 27, 
		RULE_egrep_op34 = 28, RULE_tar_op24 = 29, RULE_echo_op0 = 30, RULE_rm_op3 = 31, 
		RULE_du_op1 = 32, RULE_find_op69 = 33, RULE_find_op55 = 34, RULE_rm_op0 = 35, 
		RULE_ls_op2 = 36, RULE_egrep_op12 = 37, RULE_tar_op38 = 38, RULE_zip_op1 = 39, 
		RULE_find_op86 = 40, RULE_sort_op9 = 41, RULE_find_op45 = 42, RULE_seq_op1 = 43, 
		RULE_zip_op37 = 44, RULE_find_op27 = 45, RULE_find_op82 = 46, RULE_find_op36 = 47, 
		RULE_find_op7 = 48, RULE_xargs_op11 = 49, RULE_tar_op2 = 50, RULE_grep_op29 = 51, 
		RULE_wc_op3 = 52, RULE_find_op63 = 53, RULE_grep_op6 = 54, RULE_tar_op5 = 55, 
		RULE_xargs_op12 = 56, RULE_tar_op33 = 57, RULE_find_op2 = 58, RULE_grep_op36 = 59, 
		RULE_zip_op19 = 60, RULE_find_op24 = 61, RULE_tar_op21 = 62, RULE_sed_op2 = 63, 
		RULE_find_op71 = 64, RULE_sort_op11 = 65, RULE_find_op25 = 66, RULE_zip_op33 = 67, 
		RULE_zip_op35 = 68, RULE_chmod_op2 = 69, RULE_cp_op3 = 70, RULE_cat_op1 = 71, 
		RULE_sh_op1 = 72, RULE_find_op0 = 73, RULE_ls_op34 = 74, RULE_ls_op5 = 75, 
		RULE_egrep_op7 = 76, RULE_grep_op39 = 77, RULE_egrep_op35 = 78, RULE_find_op32 = 79, 
		RULE_grep_op22 = 80, RULE_chmod_op3 = 81, RULE_cat_op6 = 82, RULE_zip_op36 = 83, 
		RULE_tail_op0 = 84, RULE_sed_op6 = 85, RULE_tar_op44 = 86, RULE_sed_op0 = 87, 
		RULE_tar_op46 = 88, RULE_unzip_op25 = 89, RULE_find_op66 = 90, RULE_grep_op12 = 91, 
		RULE_egrep_op29 = 92, RULE_unzip_op13 = 93, RULE_cp_op0 = 94, RULE_tar_op7 = 95, 
		RULE_grep_op19 = 96, RULE_find_op12 = 97, RULE_find_op84 = 98, RULE_awk_op0 = 99, 
		RULE_find_op65 = 100, RULE_find_op13 = 101, RULE_egrep_op15 = 102, RULE_find_op42 = 103, 
		RULE_tar_op12 = 104, RULE_grep_op2 = 105, RULE_unzip_op8 = 106, RULE_du_op5 = 107, 
		RULE_find_op79 = 108, RULE_awk_op3 = 109, RULE_find_op75 = 110, RULE_cp_op5 = 111, 
		RULE_ls_op18 = 112, RULE_du_op3 = 113, RULE_ls_op25 = 114, RULE_seq_op0 = 115, 
		RULE_find_op74 = 116, RULE_find_op6 = 117, RULE_xargs_op6 = 118, RULE_sort_op14 = 119, 
		RULE_ls_op11 = 120, RULE_tar_op17 = 121, RULE_grep_op28 = 122, RULE_tail_op5 = 123, 
		RULE_tar_op43 = 124, RULE_grep_op5 = 125, RULE_egrep_op11 = 126, RULE_chmod_op11 = 127, 
		RULE_tail_op1 = 128, RULE_zip_op13 = 129, RULE_find_op57 = 130, RULE_ls_op19 = 131, 
		RULE_tar_op22 = 132, RULE_egrep_op1 = 133, RULE_find_op72 = 134, RULE_unzip_op20 = 135, 
		RULE_sed_op1 = 136, RULE_sort_op1 = 137, RULE_find_op41 = 138, RULE_grep_op37 = 139, 
		RULE_rm_op7 = 140, RULE_zip_op6 = 141, RULE_tar_op42 = 142, RULE_cat_op0 = 143, 
		RULE_cp_op8 = 144, RULE_wc_op1 = 145, RULE_tar_op18 = 146, RULE_cp_op7 = 147, 
		RULE_xargs_op13 = 148, RULE_tar_op11 = 149, RULE_chmod_op0 = 150, RULE_comm_op1 = 151, 
		RULE_grep_op32 = 152, RULE_egrep_op25 = 153, RULE_unzip_op4 = 154, RULE_tar_op30 = 155, 
		RULE_unzip_op5 = 156, RULE_seq_op3 = 157, RULE_zip_op23 = 158, RULE_zip_op17 = 159, 
		RULE_find_op33 = 160, RULE_comm_op3 = 161, RULE_du_op6 = 162, RULE_grep_op14 = 163, 
		RULE_ls_op20 = 164, RULE_wc_op4 = 165, RULE_unzip_op1 = 166, RULE_find_op56 = 167, 
		RULE_find_op85 = 168, RULE_chmod_op7 = 169, RULE_unzip_op19 = 170, RULE_ls_op8 = 171, 
		RULE_egrep_op31 = 172, RULE_ls_op29 = 173, RULE_tar_op48 = 174, RULE_sort_op18 = 175, 
		RULE_ls_op3 = 176, RULE_grep_op30 = 177, RULE_find_op58 = 178, RULE_grep_op1 = 179, 
		RULE_egrep_op6 = 180, RULE_find_op37 = 181, RULE_ls_op15 = 182, RULE_tar_op26 = 183, 
		RULE_cat_op7 = 184, RULE_ls_op14 = 185, RULE_grep_op23 = 186, RULE_tar_op8 = 187, 
		RULE_tar_op39 = 188, RULE_egrep_op39 = 189, RULE_cp_op1 = 190, RULE_find_op16 = 191, 
		RULE_ls_op24 = 192, RULE_tail_op6 = 193, RULE_tar_op0 = 194, RULE_tar_op3 = 195, 
		RULE_find_op47 = 196, RULE_tar_op9 = 197, RULE_unzip_op26 = 198, RULE_unzip_op9 = 199, 
		RULE_find_op68 = 200, RULE_zip_op38 = 201, RULE_find_op44 = 202, RULE_sort_op0 = 203, 
		RULE_find_op52 = 204, RULE_zip_op31 = 205, RULE_find_op49 = 206, RULE_unzip_op23 = 207, 
		RULE_egrep_op16 = 208, RULE_tar_op37 = 209, RULE_find_op10 = 210, RULE_zip_op0 = 211, 
		RULE_ls_op33 = 212, RULE_egrep_op38 = 213, RULE_sort_op10 = 214, RULE_zip_op27 = 215, 
		RULE_unzip_op11 = 216, RULE_find_op54 = 217, RULE_xargs_op5 = 218, RULE_egrep_op21 = 219, 
		RULE_zip_op22 = 220, RULE_find_op8 = 221, RULE_tar_op35 = 222, RULE_find_op43 = 223, 
		RULE_unzip_op14 = 224, RULE_grep_op18 = 225, RULE_head_op0 = 226, RULE_egrep_op26 = 227, 
		RULE_zip_op5 = 228, RULE_xargs_op2 = 229, RULE_grep_op13 = 230, RULE_unzip_op17 = 231, 
		RULE_find_op64 = 232, RULE_mv_op1 = 233, RULE_find_op50 = 234, RULE_zip_op34 = 235, 
		RULE_chown_op3 = 236, RULE_find_op40 = 237, RULE_sort_op13 = 238, RULE_zip_op7 = 239, 
		RULE_find_op48 = 240, RULE_wc_op2 = 241, RULE_find_op11 = 242, RULE_tail_op2 = 243, 
		RULE_sed_op7 = 244, RULE_grep_op4 = 245, RULE_seq_op5 = 246, RULE_find_op77 = 247, 
		RULE_zip_op30 = 248, RULE_tar_op29 = 249, RULE_chmod_op6 = 250, RULE_chmod_op9 = 251, 
		RULE_find_op28 = 252, RULE_cp_op4 = 253, RULE_egrep_op10 = 254, RULE_find_op70 = 255, 
		RULE_head_op3 = 256, RULE_xargs_op0 = 257, RULE_awk_op1 = 258, RULE_ls_op36 = 259, 
		RULE_find_op81 = 260, RULE_grep_op20 = 261, RULE_tail_op3 = 262, RULE_find_op61 = 263, 
		RULE_tar_op40 = 264, RULE_grep_op38 = 265, RULE_rm_op2 = 266, RULE_mv_op0 = 267, 
		RULE_grep_op34 = 268, RULE_tar_op20 = 269, RULE_grep_op17 = 270, RULE_find_op31 = 271, 
		RULE_ls_op7 = 272, RULE_ls_op37 = 273, RULE_tar_op25 = 274, RULE_awk_op4 = 275, 
		RULE_ls_op4 = 276, RULE_comm_op0 = 277, RULE_grep_op27 = 278, RULE_find_op35 = 279, 
		RULE_find_op59 = 280, RULE_egrep_op24 = 281, RULE_sort_op4 = 282, RULE_tar_op31 = 283, 
		RULE_unzip_op6 = 284, RULE_grep_op33 = 285, RULE_egrep_op2 = 286, RULE_zip_op24 = 287, 
		RULE_cd_op1 = 288, RULE_rm_op4 = 289, RULE_tar_op14 = 290, RULE_head_op2 = 291, 
		RULE_du_op2 = 292, RULE_ls_op0 = 293, RULE_zip_op10 = 294, RULE_sort_op7 = 295, 
		RULE_sed_op5 = 296, RULE_egrep_op18 = 297, RULE_tar_op36 = 298, RULE_egrep_op13 = 299, 
		RULE_egrep_op20 = 300, RULE_zip_op18 = 301, RULE_ls_op16 = 302, RULE_tar_op10 = 303, 
		RULE_find_op17 = 304, RULE_grep_op0 = 305, RULE_find_op73 = 306, RULE_find_op53 = 307, 
		RULE_find_op3 = 308, RULE_cp_op6 = 309, RULE_tar_op27 = 310, RULE_chown_op1 = 311, 
		RULE_echo_op1 = 312, RULE_tar_op4 = 313, RULE_unzip_op10 = 314, RULE_tar_op1 = 315, 
		RULE_xargs_op3 = 316, RULE_seq_op4 = 317, RULE_chmod_op8 = 318, RULE_find_op67 = 319, 
		RULE_egrep_op17 = 320, RULE_cat_op2 = 321, RULE_sort_op17 = 322, RULE_ls_op23 = 323, 
		RULE_wc_op0 = 324, RULE_chmod_op4 = 325, RULE_grep_op24 = 326, RULE_zip_op28 = 327, 
		RULE_unzip_op22 = 328, RULE_find_op34 = 329, RULE_zip_op4 = 330, RULE_egrep_op27 = 331, 
		RULE_xargs_op1 = 332, RULE_ls_op32 = 333, RULE_find_op76 = 334, RULE_grep_op40 = 335, 
		RULE_egrep_op5 = 336, RULE_ls_op10 = 337, RULE_unzip_op15 = 338, RULE_grep_op35 = 339, 
		RULE_cat_op4 = 340, RULE_tar_op16 = 341, RULE_zip_op14 = 342, RULE_zip_op21 = 343, 
		RULE_unzip_op24 = 344, RULE_find_op9 = 345, RULE_find_op60 = 346, RULE_zip_op8 = 347, 
		RULE_rm_op1 = 348, RULE_tar_op19 = 349, RULE_ls_op30 = 350, RULE_sort_op6 = 351, 
		RULE_zip_op25 = 352, RULE_ls_op22 = 353, RULE_find_op83 = 354, RULE_tar_op32 = 355, 
		RULE_grep_op16 = 356, RULE_find_op39 = 357, RULE_grep_op9 = 358, RULE_find_op18 = 359, 
		RULE_grep_op7 = 360, RULE_du_op7 = 361, RULE_sort_op12 = 362, RULE_cp_op2 = 363, 
		RULE_find_op4 = 364, RULE_find_op19 = 365, RULE_ls_op27 = 366, RULE_zip_op2 = 367, 
		RULE_zip_op40 = 368, RULE_du_op4 = 369, RULE_find_op80 = 370, RULE_tar_op45 = 371, 
		RULE_grep_op26 = 372, RULE_sed_op3 = 373, RULE_xargs_op4 = 374, RULE_xargs_op7 = 375, 
		RULE_zip_op32 = 376, RULE_tar_op15 = 377, RULE_grep_op10 = 378, RULE_egrep_op3 = 379, 
		RULE_ls_op35 = 380, RULE_tar_op23 = 381, RULE_find_op5 = 382, RULE_egrep_op23 = 383, 
		RULE_egrep_op32 = 384, RULE_awk_op5 = 385, RULE_sort_op16 = 386, RULE_find_op23 = 387, 
		RULE_seq_op2 = 388, RULE_find_op1 = 389, RULE_zip_op39 = 390, RULE_sh_op0 = 391, 
		RULE_sort_op3 = 392, RULE_ls_op9 = 393, RULE_ls_op1 = 394, RULE_find_op78 = 395, 
		RULE_grep_op31 = 396, RULE_ls_op6 = 397, RULE_sed_op4 = 398, RULE_cd_op0 = 399, 
		RULE_grep_op21 = 400, RULE_egrep_op37 = 401, RULE_find_op46 = 402, RULE_tar_op34 = 403, 
		RULE_egrep_op30 = 404, RULE_egrep_op9 = 405, RULE_chown_op2 = 406, RULE_diff_op0 = 407, 
		RULE_xargs_op8 = 408, RULE_sort_op8 = 409, RULE_tar_op6 = 410, RULE_ls_op13 = 411, 
		RULE_unzip_op0 = 412, RULE_egrep_op19 = 413, RULE_find_op14 = 414, RULE_find_op62 = 415, 
		RULE_ls_op38 = 416, RULE_chown_op0 = 417, RULE_find_op20 = 418, RULE_zip_op11 = 419, 
		RULE_egrep_op8 = 420, RULE_chmod_op10 = 421, RULE_egrep_op28 = 422, RULE_zip_op29 = 423, 
		RULE_egrep_op4 = 424, RULE_zip_op3 = 425, RULE_ls_op17 = 426, RULE_find_op21 = 427, 
		RULE_grep_op3 = 428, RULE_unzip_op7 = 429, RULE_grep_op8 = 430, RULE_tar_op41 = 431, 
		RULE_cp_op9 = 432, RULE_cat_op5 = 433, RULE_zip_op20 = 434, RULE_egrep_op40 = 435, 
		RULE_zip_op15 = 436, RULE_unzip_op12 = 437, RULE_find_op30 = 438, RULE_ls_op26 = 439, 
		RULE_unzip_op3 = 440, RULE_tar_op28 = 441, RULE_chown_op4 = 442, RULE_find_op22 = 443, 
		RULE_head_op1 = 444, RULE_rm_op5 = 445, RULE_unzip_op21 = 446, RULE_find_op26 = 447, 
		RULE_awk_op2 = 448, RULE_egrep_op33 = 449, RULE_grep_op25 = 450, RULE_unzip_op16 = 451, 
		RULE_du_op0 = 452, RULE_xargs_op14 = 453, RULE_find_op29 = 454, RULE_tar_op13 = 455, 
		RULE_grep_op11 = 456, RULE_egrep_op36 = 457, RULE_egrep_op14 = 458, RULE_ls_op31 = 459;
	public static final String[] ruleNames = {
		"command", "tar_op47", "unzip_op2", "grep_op15", "ls_op21", "cat_op3", 
		"sort_op2", "unzip_op18", "ls_op28", "zip_op26", "sort_op5", "tail_op4", 
		"find_op15", "xargs_op10", "find_op51", "zip_op16", "xargs_op9", "find_op38", 
		"sort_op15", "ls_op12", "chmod_op1", "comm_op2", "egrep_op0", "rm_op6", 
		"zip_op9", "zip_op12", "chmod_op5", "egrep_op22", "egrep_op34", "tar_op24", 
		"echo_op0", "rm_op3", "du_op1", "find_op69", "find_op55", "rm_op0", "ls_op2", 
		"egrep_op12", "tar_op38", "zip_op1", "find_op86", "sort_op9", "find_op45", 
		"seq_op1", "zip_op37", "find_op27", "find_op82", "find_op36", "find_op7", 
		"xargs_op11", "tar_op2", "grep_op29", "wc_op3", "find_op63", "grep_op6", 
		"tar_op5", "xargs_op12", "tar_op33", "find_op2", "grep_op36", "zip_op19", 
		"find_op24", "tar_op21", "sed_op2", "find_op71", "sort_op11", "find_op25", 
		"zip_op33", "zip_op35", "chmod_op2", "cp_op3", "cat_op1", "sh_op1", "find_op0", 
		"ls_op34", "ls_op5", "egrep_op7", "grep_op39", "egrep_op35", "find_op32", 
		"grep_op22", "chmod_op3", "cat_op6", "zip_op36", "tail_op0", "sed_op6", 
		"tar_op44", "sed_op0", "tar_op46", "unzip_op25", "find_op66", "grep_op12", 
		"egrep_op29", "unzip_op13", "cp_op0", "tar_op7", "grep_op19", "find_op12", 
		"find_op84", "awk_op0", "find_op65", "find_op13", "egrep_op15", "find_op42", 
		"tar_op12", "grep_op2", "unzip_op8", "du_op5", "find_op79", "awk_op3", 
		"find_op75", "cp_op5", "ls_op18", "du_op3", "ls_op25", "seq_op0", "find_op74", 
		"find_op6", "xargs_op6", "sort_op14", "ls_op11", "tar_op17", "grep_op28", 
		"tail_op5", "tar_op43", "grep_op5", "egrep_op11", "chmod_op11", "tail_op1", 
		"zip_op13", "find_op57", "ls_op19", "tar_op22", "egrep_op1", "find_op72", 
		"unzip_op20", "sed_op1", "sort_op1", "find_op41", "grep_op37", "rm_op7", 
		"zip_op6", "tar_op42", "cat_op0", "cp_op8", "wc_op1", "tar_op18", "cp_op7", 
		"xargs_op13", "tar_op11", "chmod_op0", "comm_op1", "grep_op32", "egrep_op25", 
		"unzip_op4", "tar_op30", "unzip_op5", "seq_op3", "zip_op23", "zip_op17", 
		"find_op33", "comm_op3", "du_op6", "grep_op14", "ls_op20", "wc_op4", "unzip_op1", 
		"find_op56", "find_op85", "chmod_op7", "unzip_op19", "ls_op8", "egrep_op31", 
		"ls_op29", "tar_op48", "sort_op18", "ls_op3", "grep_op30", "find_op58", 
		"grep_op1", "egrep_op6", "find_op37", "ls_op15", "tar_op26", "cat_op7", 
		"ls_op14", "grep_op23", "tar_op8", "tar_op39", "egrep_op39", "cp_op1", 
		"find_op16", "ls_op24", "tail_op6", "tar_op0", "tar_op3", "find_op47", 
		"tar_op9", "unzip_op26", "unzip_op9", "find_op68", "zip_op38", "find_op44", 
		"sort_op0", "find_op52", "zip_op31", "find_op49", "unzip_op23", "egrep_op16", 
		"tar_op37", "find_op10", "zip_op0", "ls_op33", "egrep_op38", "sort_op10", 
		"zip_op27", "unzip_op11", "find_op54", "xargs_op5", "egrep_op21", "zip_op22", 
		"find_op8", "tar_op35", "find_op43", "unzip_op14", "grep_op18", "head_op0", 
		"egrep_op26", "zip_op5", "xargs_op2", "grep_op13", "unzip_op17", "find_op64", 
		"mv_op1", "find_op50", "zip_op34", "chown_op3", "find_op40", "sort_op13", 
		"zip_op7", "find_op48", "wc_op2", "find_op11", "tail_op2", "sed_op7", 
		"grep_op4", "seq_op5", "find_op77", "zip_op30", "tar_op29", "chmod_op6", 
		"chmod_op9", "find_op28", "cp_op4", "egrep_op10", "find_op70", "head_op3", 
		"xargs_op0", "awk_op1", "ls_op36", "find_op81", "grep_op20", "tail_op3", 
		"find_op61", "tar_op40", "grep_op38", "rm_op2", "mv_op0", "grep_op34", 
		"tar_op20", "grep_op17", "find_op31", "ls_op7", "ls_op37", "tar_op25", 
		"awk_op4", "ls_op4", "comm_op0", "grep_op27", "find_op35", "find_op59", 
		"egrep_op24", "sort_op4", "tar_op31", "unzip_op6", "grep_op33", "egrep_op2", 
		"zip_op24", "cd_op1", "rm_op4", "tar_op14", "head_op2", "du_op2", "ls_op0", 
		"zip_op10", "sort_op7", "sed_op5", "egrep_op18", "tar_op36", "egrep_op13", 
		"egrep_op20", "zip_op18", "ls_op16", "tar_op10", "find_op17", "grep_op0", 
		"find_op73", "find_op53", "find_op3", "cp_op6", "tar_op27", "chown_op1", 
		"echo_op1", "tar_op4", "unzip_op10", "tar_op1", "xargs_op3", "seq_op4", 
		"chmod_op8", "find_op67", "egrep_op17", "cat_op2", "sort_op17", "ls_op23", 
		"wc_op0", "chmod_op4", "grep_op24", "zip_op28", "unzip_op22", "find_op34", 
		"zip_op4", "egrep_op27", "xargs_op1", "ls_op32", "find_op76", "grep_op40", 
		"egrep_op5", "ls_op10", "unzip_op15", "grep_op35", "cat_op4", "tar_op16", 
		"zip_op14", "zip_op21", "unzip_op24", "find_op9", "find_op60", "zip_op8", 
		"rm_op1", "tar_op19", "ls_op30", "sort_op6", "zip_op25", "ls_op22", "find_op83", 
		"tar_op32", "grep_op16", "find_op39", "grep_op9", "find_op18", "grep_op7", 
		"du_op7", "sort_op12", "cp_op2", "find_op4", "find_op19", "ls_op27", "zip_op2", 
		"zip_op40", "du_op4", "find_op80", "tar_op45", "grep_op26", "sed_op3", 
		"xargs_op4", "xargs_op7", "zip_op32", "tar_op15", "grep_op10", "egrep_op3", 
		"ls_op35", "tar_op23", "find_op5", "egrep_op23", "egrep_op32", "awk_op5", 
		"sort_op16", "find_op23", "seq_op2", "find_op1", "zip_op39", "sh_op0", 
		"sort_op3", "ls_op9", "ls_op1", "find_op78", "grep_op31", "ls_op6", "sed_op4", 
		"cd_op0", "grep_op21", "egrep_op37", "find_op46", "tar_op34", "egrep_op30", 
		"egrep_op9", "chown_op2", "diff_op0", "xargs_op8", "sort_op8", "tar_op6", 
		"ls_op13", "unzip_op0", "egrep_op19", "find_op14", "find_op62", "ls_op38", 
		"chown_op0", "find_op20", "zip_op11", "egrep_op8", "chmod_op10", "egrep_op28", 
		"zip_op29", "egrep_op4", "zip_op3", "ls_op17", "find_op21", "grep_op3", 
		"unzip_op7", "grep_op8", "tar_op41", "cp_op9", "cat_op5", "zip_op20", 
		"egrep_op40", "zip_op15", "unzip_op12", "find_op30", "ls_op26", "unzip_op3", 
		"tar_op28", "chown_op4", "find_op22", "head_op1", "rm_op5", "unzip_op21", 
		"find_op26", "awk_op2", "egrep_op33", "grep_op25", "unzip_op16", "du_op0", 
		"xargs_op14", "find_op29", "tar_op13", "grep_op11", "egrep_op36", "egrep_op14", 
		"ls_op31"
	};

	private static final String[] _LITERAL_NAMES = {
		null, "'find'", "'-f'", "'mv'", "'sort'", "'grep'", "'egrep'", "'cp'", 
		"'ls'", "'tar'", "'-c'", "'-r'", "'-u'", "'-t'", "'-x'", "'xargs'", "'sed'", 
		"'awk'", "'rm'", "'cd'", "'wc'", "'chmod'", "'ACE'", "'chown'", "'head'", 
		"'tail'", "'seq'", "'unlink'", "'cat'", "'zip'", "'unzip'", "'du'", "'echo'", 
		"'diff'", "'comm'", "'sh'", "'--strip-components'", "'-m'", "'-g'", "'-s'", 
		"'-K'", "'-o'", "'-w'", "'-M'", "'-n'", "'-anewer'", "'-mmin'", "'-group'", 
		"'-T'", "'-U'", "'-v'", "'-3'", "'-a'", "'-F'", "'-j'", "'+'", "'-S'", 
		"'-P'", "'-d'", "'-print0'", "'-name'", "'-C'", "'-J'", "'-q'", "'-A'", 
		"'-k'", "'-iwholename'", "'-empty'", "'-and'", "'-fstype'", "'-true'", 
		"'--check-links'", "'-Z'", "'-okdir'", "';'", "'-X'", "'--label'", "'-delete'", 
		"'--options'", "'-l'", "'-prune'", "'-depth'", "'--longoption'", "'-H'", 
		"'-L'", "'-i'", "'-e'", "'-G'", "'--context='", "'-execdir'", "'-R'", 
		"'--numeric-owner'", "'-E'", "'-perm'", "'-'", "'-h'", "'-p'", "'-Btime'", 
		"'-not'", "'-acl'", "'-inum'", "'-wholename'", "'-type'", "'-size'", "'-I'", 
		"'--newer-mtime-than'", "'-N'", "'-newerXY'", "'-b'", "'-regex'", "'-iname'", 
		"'--line-buffered'", "'-W'", "'--keep-newer-files'", "'--nodump'", "'-2'", 
		"'-V'", "'-y'", "'-flags'", "'-newer'", "'!'", "'-B'", "'-nogroup'", "'-gid'", 
		"'-@'", "'--exclude'", "'-lname'", "'--include'", "'-z'", "'-print'", 
		"'-iregex'", "'-mnewer'", "'-!'", "'-maxdepth'", "'-O'", "'-Bmin'", "'--null'", 
		"'-mtime'", "'-false'", "'-ipath'", "'-D'", "'-path'", "'-mindepth'", 
		"'-ilname'", "'-ls'", "'-Bnewer'", "'-uid'", "'='", "'-printf'", "'-0'", 
		"'-xattrname'", "'-nouser'", "'--chroot'", "'--one-file-system'", "'-1'", 
		"'--use-compress-program'", "'-noignore_readdir_race'", "'--newer'", "'--format'", 
		"'-cmin'", "'-samefile'", "'-mount'", "'--version'", "'--newer-than'", 
		"'-noleaf'", "'-or'", "'-ignore_readdir_race'", "'-cnewer'", "'-ctime'", 
		"'-xi'", "'-xattr'", "'-$'", "'--newer-mtime'", "'-user'", "'-links'", 
		"'-amin'", "'-ok'", "'-exec'", "'{}'"
	};
	private static final String[] _SYMBOLIC_NAMES = {
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, null, 
		null, null, null, null, null, null, null, null, null, null, null, "STRING", 
		"WS"
	};
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "Commands.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public CommandsParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class CommandContext extends ParserRuleContext {
		public Token File;
		public Token String;
		public Token Permission;
		public Find_op0Context find_op0() {
			return getRuleContext(Find_op0Context.class,0);
		}
		public Find_op1Context find_op1() {
			return getRuleContext(Find_op1Context.class,0);
		}
		public Find_op2Context find_op2() {
			return getRuleContext(Find_op2Context.class,0);
		}
		public List<Find_op3Context> find_op3() {
			return getRuleContexts(Find_op3Context.class);
		}
		public Find_op3Context find_op3(int i) {
			return getRuleContext(Find_op3Context.class,i);
		}
		public List<Find_op4Context> find_op4() {
			return getRuleContexts(Find_op4Context.class);
		}
		public Find_op4Context find_op4(int i) {
			return getRuleContext(Find_op4Context.class,i);
		}
		public Find_op5Context find_op5() {
			return getRuleContext(Find_op5Context.class,0);
		}
		public Find_op6Context find_op6() {
			return getRuleContext(Find_op6Context.class,0);
		}
		public Find_op7Context find_op7() {
			return getRuleContext(Find_op7Context.class,0);
		}
		public Find_op8Context find_op8() {
			return getRuleContext(Find_op8Context.class,0);
		}
		public Find_op9Context find_op9() {
			return getRuleContext(Find_op9Context.class,0);
		}
		public Find_op10Context find_op10() {
			return getRuleContext(Find_op10Context.class,0);
		}
		public Find_op11Context find_op11() {
			return getRuleContext(Find_op11Context.class,0);
		}
		public Find_op12Context find_op12() {
			return getRuleContext(Find_op12Context.class,0);
		}
		public Find_op13Context find_op13() {
			return getRuleContext(Find_op13Context.class,0);
		}
		public Find_op14Context find_op14() {
			return getRuleContext(Find_op14Context.class,0);
		}
		public Find_op15Context find_op15() {
			return getRuleContext(Find_op15Context.class,0);
		}
		public Find_op16Context find_op16() {
			return getRuleContext(Find_op16Context.class,0);
		}
		public Find_op17Context find_op17() {
			return getRuleContext(Find_op17Context.class,0);
		}
		public Find_op18Context find_op18() {
			return getRuleContext(Find_op18Context.class,0);
		}
		public Find_op19Context find_op19() {
			return getRuleContext(Find_op19Context.class,0);
		}
		public List<Find_op20Context> find_op20() {
			return getRuleContexts(Find_op20Context.class);
		}
		public Find_op20Context find_op20(int i) {
			return getRuleContext(Find_op20Context.class,i);
		}
		public Find_op21Context find_op21() {
			return getRuleContext(Find_op21Context.class,0);
		}
		public List<Find_op22Context> find_op22() {
			return getRuleContexts(Find_op22Context.class);
		}
		public Find_op22Context find_op22(int i) {
			return getRuleContext(Find_op22Context.class,i);
		}
		public Find_op23Context find_op23() {
			return getRuleContext(Find_op23Context.class,0);
		}
		public Find_op24Context find_op24() {
			return getRuleContext(Find_op24Context.class,0);
		}
		public Find_op25Context find_op25() {
			return getRuleContext(Find_op25Context.class,0);
		}
		public Find_op26Context find_op26() {
			return getRuleContext(Find_op26Context.class,0);
		}
		public Find_op27Context find_op27() {
			return getRuleContext(Find_op27Context.class,0);
		}
		public Find_op29Context find_op29() {
			return getRuleContext(Find_op29Context.class,0);
		}
		public Find_op30Context find_op30() {
			return getRuleContext(Find_op30Context.class,0);
		}
		public Find_op31Context find_op31() {
			return getRuleContext(Find_op31Context.class,0);
		}
		public Find_op32Context find_op32() {
			return getRuleContext(Find_op32Context.class,0);
		}
		public Find_op33Context find_op33() {
			return getRuleContext(Find_op33Context.class,0);
		}
		public Find_op34Context find_op34() {
			return getRuleContext(Find_op34Context.class,0);
		}
		public Find_op35Context find_op35() {
			return getRuleContext(Find_op35Context.class,0);
		}
		public Find_op36Context find_op36() {
			return getRuleContext(Find_op36Context.class,0);
		}
		public Find_op37Context find_op37() {
			return getRuleContext(Find_op37Context.class,0);
		}
		public Find_op38Context find_op38() {
			return getRuleContext(Find_op38Context.class,0);
		}
		public Find_op39Context find_op39() {
			return getRuleContext(Find_op39Context.class,0);
		}
		public List<Find_op40Context> find_op40() {
			return getRuleContexts(Find_op40Context.class);
		}
		public Find_op40Context find_op40(int i) {
			return getRuleContext(Find_op40Context.class,i);
		}
		public Find_op41Context find_op41() {
			return getRuleContext(Find_op41Context.class,0);
		}
		public Find_op42Context find_op42() {
			return getRuleContext(Find_op42Context.class,0);
		}
		public Find_op43Context find_op43() {
			return getRuleContext(Find_op43Context.class,0);
		}
		public Find_op44Context find_op44() {
			return getRuleContext(Find_op44Context.class,0);
		}
		public Find_op45Context find_op45() {
			return getRuleContext(Find_op45Context.class,0);
		}
		public Find_op46Context find_op46() {
			return getRuleContext(Find_op46Context.class,0);
		}
		public Find_op47Context find_op47() {
			return getRuleContext(Find_op47Context.class,0);
		}
		public Find_op48Context find_op48() {
			return getRuleContext(Find_op48Context.class,0);
		}
		public Find_op49Context find_op49() {
			return getRuleContext(Find_op49Context.class,0);
		}
		public Find_op50Context find_op50() {
			return getRuleContext(Find_op50Context.class,0);
		}
		public Find_op51Context find_op51() {
			return getRuleContext(Find_op51Context.class,0);
		}
		public Find_op52Context find_op52() {
			return getRuleContext(Find_op52Context.class,0);
		}
		public Find_op53Context find_op53() {
			return getRuleContext(Find_op53Context.class,0);
		}
		public Find_op54Context find_op54() {
			return getRuleContext(Find_op54Context.class,0);
		}
		public Find_op55Context find_op55() {
			return getRuleContext(Find_op55Context.class,0);
		}
		public Find_op56Context find_op56() {
			return getRuleContext(Find_op56Context.class,0);
		}
		public Find_op57Context find_op57() {
			return getRuleContext(Find_op57Context.class,0);
		}
		public Find_op58Context find_op58() {
			return getRuleContext(Find_op58Context.class,0);
		}
		public Find_op59Context find_op59() {
			return getRuleContext(Find_op59Context.class,0);
		}
		public Find_op60Context find_op60() {
			return getRuleContext(Find_op60Context.class,0);
		}
		public Find_op61Context find_op61() {
			return getRuleContext(Find_op61Context.class,0);
		}
		public Find_op62Context find_op62() {
			return getRuleContext(Find_op62Context.class,0);
		}
		public Find_op63Context find_op63() {
			return getRuleContext(Find_op63Context.class,0);
		}
		public Find_op64Context find_op64() {
			return getRuleContext(Find_op64Context.class,0);
		}
		public Find_op65Context find_op65() {
			return getRuleContext(Find_op65Context.class,0);
		}
		public Find_op66Context find_op66() {
			return getRuleContext(Find_op66Context.class,0);
		}
		public Find_op67Context find_op67() {
			return getRuleContext(Find_op67Context.class,0);
		}
		public Find_op68Context find_op68() {
			return getRuleContext(Find_op68Context.class,0);
		}
		public Find_op69Context find_op69() {
			return getRuleContext(Find_op69Context.class,0);
		}
		public Find_op70Context find_op70() {
			return getRuleContext(Find_op70Context.class,0);
		}
		public Find_op71Context find_op71() {
			return getRuleContext(Find_op71Context.class,0);
		}
		public Find_op72Context find_op72() {
			return getRuleContext(Find_op72Context.class,0);
		}
		public Find_op73Context find_op73() {
			return getRuleContext(Find_op73Context.class,0);
		}
		public Find_op74Context find_op74() {
			return getRuleContext(Find_op74Context.class,0);
		}
		public Find_op75Context find_op75() {
			return getRuleContext(Find_op75Context.class,0);
		}
		public Find_op76Context find_op76() {
			return getRuleContext(Find_op76Context.class,0);
		}
		public Find_op77Context find_op77() {
			return getRuleContext(Find_op77Context.class,0);
		}
		public Find_op78Context find_op78() {
			return getRuleContext(Find_op78Context.class,0);
		}
		public Find_op79Context find_op79() {
			return getRuleContext(Find_op79Context.class,0);
		}
		public Find_op80Context find_op80() {
			return getRuleContext(Find_op80Context.class,0);
		}
		public Find_op81Context find_op81() {
			return getRuleContext(Find_op81Context.class,0);
		}
		public Find_op82Context find_op82() {
			return getRuleContext(Find_op82Context.class,0);
		}
		public Find_op83Context find_op83() {
			return getRuleContext(Find_op83Context.class,0);
		}
		public Find_op84Context find_op84() {
			return getRuleContext(Find_op84Context.class,0);
		}
		public Find_op85Context find_op85() {
			return getRuleContext(Find_op85Context.class,0);
		}
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Find_op86Context find_op86() {
			return getRuleContext(Find_op86Context.class,0);
		}
		public Mv_op0Context mv_op0() {
			return getRuleContext(Mv_op0Context.class,0);
		}
		public Mv_op1Context mv_op1() {
			return getRuleContext(Mv_op1Context.class,0);
		}
		public Sort_op0Context sort_op0() {
			return getRuleContext(Sort_op0Context.class,0);
		}
		public Sort_op1Context sort_op1() {
			return getRuleContext(Sort_op1Context.class,0);
		}
		public Sort_op2Context sort_op2() {
			return getRuleContext(Sort_op2Context.class,0);
		}
		public Sort_op3Context sort_op3() {
			return getRuleContext(Sort_op3Context.class,0);
		}
		public Sort_op4Context sort_op4() {
			return getRuleContext(Sort_op4Context.class,0);
		}
		public Sort_op5Context sort_op5() {
			return getRuleContext(Sort_op5Context.class,0);
		}
		public Sort_op6Context sort_op6() {
			return getRuleContext(Sort_op6Context.class,0);
		}
		public Sort_op7Context sort_op7() {
			return getRuleContext(Sort_op7Context.class,0);
		}
		public Sort_op8Context sort_op8() {
			return getRuleContext(Sort_op8Context.class,0);
		}
		public Sort_op9Context sort_op9() {
			return getRuleContext(Sort_op9Context.class,0);
		}
		public Sort_op10Context sort_op10() {
			return getRuleContext(Sort_op10Context.class,0);
		}
		public Sort_op11Context sort_op11() {
			return getRuleContext(Sort_op11Context.class,0);
		}
		public Sort_op12Context sort_op12() {
			return getRuleContext(Sort_op12Context.class,0);
		}
		public Sort_op13Context sort_op13() {
			return getRuleContext(Sort_op13Context.class,0);
		}
		public Sort_op14Context sort_op14() {
			return getRuleContext(Sort_op14Context.class,0);
		}
		public Sort_op15Context sort_op15() {
			return getRuleContext(Sort_op15Context.class,0);
		}
		public Sort_op16Context sort_op16() {
			return getRuleContext(Sort_op16Context.class,0);
		}
		public Sort_op17Context sort_op17() {
			return getRuleContext(Sort_op17Context.class,0);
		}
		public Sort_op18Context sort_op18() {
			return getRuleContext(Sort_op18Context.class,0);
		}
		public Grep_op0Context grep_op0() {
			return getRuleContext(Grep_op0Context.class,0);
		}
		public Grep_op1Context grep_op1() {
			return getRuleContext(Grep_op1Context.class,0);
		}
		public Grep_op2Context grep_op2() {
			return getRuleContext(Grep_op2Context.class,0);
		}
		public Grep_op3Context grep_op3() {
			return getRuleContext(Grep_op3Context.class,0);
		}
		public Grep_op4Context grep_op4() {
			return getRuleContext(Grep_op4Context.class,0);
		}
		public Grep_op5Context grep_op5() {
			return getRuleContext(Grep_op5Context.class,0);
		}
		public Grep_op6Context grep_op6() {
			return getRuleContext(Grep_op6Context.class,0);
		}
		public Grep_op7Context grep_op7() {
			return getRuleContext(Grep_op7Context.class,0);
		}
		public Grep_op8Context grep_op8() {
			return getRuleContext(Grep_op8Context.class,0);
		}
		public Grep_op9Context grep_op9() {
			return getRuleContext(Grep_op9Context.class,0);
		}
		public Grep_op10Context grep_op10() {
			return getRuleContext(Grep_op10Context.class,0);
		}
		public Grep_op11Context grep_op11() {
			return getRuleContext(Grep_op11Context.class,0);
		}
		public Grep_op12Context grep_op12() {
			return getRuleContext(Grep_op12Context.class,0);
		}
		public Grep_op13Context grep_op13() {
			return getRuleContext(Grep_op13Context.class,0);
		}
		public Grep_op14Context grep_op14() {
			return getRuleContext(Grep_op14Context.class,0);
		}
		public Grep_op15Context grep_op15() {
			return getRuleContext(Grep_op15Context.class,0);
		}
		public Grep_op16Context grep_op16() {
			return getRuleContext(Grep_op16Context.class,0);
		}
		public Grep_op17Context grep_op17() {
			return getRuleContext(Grep_op17Context.class,0);
		}
		public Grep_op18Context grep_op18() {
			return getRuleContext(Grep_op18Context.class,0);
		}
		public Grep_op19Context grep_op19() {
			return getRuleContext(Grep_op19Context.class,0);
		}
		public Grep_op20Context grep_op20() {
			return getRuleContext(Grep_op20Context.class,0);
		}
		public Grep_op21Context grep_op21() {
			return getRuleContext(Grep_op21Context.class,0);
		}
		public Grep_op22Context grep_op22() {
			return getRuleContext(Grep_op22Context.class,0);
		}
		public Grep_op23Context grep_op23() {
			return getRuleContext(Grep_op23Context.class,0);
		}
		public Grep_op24Context grep_op24() {
			return getRuleContext(Grep_op24Context.class,0);
		}
		public Grep_op25Context grep_op25() {
			return getRuleContext(Grep_op25Context.class,0);
		}
		public Grep_op26Context grep_op26() {
			return getRuleContext(Grep_op26Context.class,0);
		}
		public Grep_op27Context grep_op27() {
			return getRuleContext(Grep_op27Context.class,0);
		}
		public Grep_op28Context grep_op28() {
			return getRuleContext(Grep_op28Context.class,0);
		}
		public Grep_op29Context grep_op29() {
			return getRuleContext(Grep_op29Context.class,0);
		}
		public Grep_op30Context grep_op30() {
			return getRuleContext(Grep_op30Context.class,0);
		}
		public Grep_op31Context grep_op31() {
			return getRuleContext(Grep_op31Context.class,0);
		}
		public Grep_op32Context grep_op32() {
			return getRuleContext(Grep_op32Context.class,0);
		}
		public Grep_op33Context grep_op33() {
			return getRuleContext(Grep_op33Context.class,0);
		}
		public Grep_op34Context grep_op34() {
			return getRuleContext(Grep_op34Context.class,0);
		}
		public Grep_op35Context grep_op35() {
			return getRuleContext(Grep_op35Context.class,0);
		}
		public Grep_op36Context grep_op36() {
			return getRuleContext(Grep_op36Context.class,0);
		}
		public Grep_op37Context grep_op37() {
			return getRuleContext(Grep_op37Context.class,0);
		}
		public Grep_op38Context grep_op38() {
			return getRuleContext(Grep_op38Context.class,0);
		}
		public Grep_op39Context grep_op39() {
			return getRuleContext(Grep_op39Context.class,0);
		}
		public Grep_op40Context grep_op40() {
			return getRuleContext(Grep_op40Context.class,0);
		}
		public Egrep_op0Context egrep_op0() {
			return getRuleContext(Egrep_op0Context.class,0);
		}
		public Egrep_op1Context egrep_op1() {
			return getRuleContext(Egrep_op1Context.class,0);
		}
		public Egrep_op2Context egrep_op2() {
			return getRuleContext(Egrep_op2Context.class,0);
		}
		public Egrep_op3Context egrep_op3() {
			return getRuleContext(Egrep_op3Context.class,0);
		}
		public Egrep_op4Context egrep_op4() {
			return getRuleContext(Egrep_op4Context.class,0);
		}
		public Egrep_op5Context egrep_op5() {
			return getRuleContext(Egrep_op5Context.class,0);
		}
		public Egrep_op6Context egrep_op6() {
			return getRuleContext(Egrep_op6Context.class,0);
		}
		public Egrep_op7Context egrep_op7() {
			return getRuleContext(Egrep_op7Context.class,0);
		}
		public Egrep_op8Context egrep_op8() {
			return getRuleContext(Egrep_op8Context.class,0);
		}
		public Egrep_op9Context egrep_op9() {
			return getRuleContext(Egrep_op9Context.class,0);
		}
		public Egrep_op10Context egrep_op10() {
			return getRuleContext(Egrep_op10Context.class,0);
		}
		public Egrep_op11Context egrep_op11() {
			return getRuleContext(Egrep_op11Context.class,0);
		}
		public Egrep_op12Context egrep_op12() {
			return getRuleContext(Egrep_op12Context.class,0);
		}
		public Egrep_op13Context egrep_op13() {
			return getRuleContext(Egrep_op13Context.class,0);
		}
		public Egrep_op14Context egrep_op14() {
			return getRuleContext(Egrep_op14Context.class,0);
		}
		public Egrep_op15Context egrep_op15() {
			return getRuleContext(Egrep_op15Context.class,0);
		}
		public Egrep_op16Context egrep_op16() {
			return getRuleContext(Egrep_op16Context.class,0);
		}
		public Egrep_op17Context egrep_op17() {
			return getRuleContext(Egrep_op17Context.class,0);
		}
		public Egrep_op18Context egrep_op18() {
			return getRuleContext(Egrep_op18Context.class,0);
		}
		public Egrep_op19Context egrep_op19() {
			return getRuleContext(Egrep_op19Context.class,0);
		}
		public Egrep_op20Context egrep_op20() {
			return getRuleContext(Egrep_op20Context.class,0);
		}
		public Egrep_op21Context egrep_op21() {
			return getRuleContext(Egrep_op21Context.class,0);
		}
		public Egrep_op22Context egrep_op22() {
			return getRuleContext(Egrep_op22Context.class,0);
		}
		public Egrep_op23Context egrep_op23() {
			return getRuleContext(Egrep_op23Context.class,0);
		}
		public Egrep_op24Context egrep_op24() {
			return getRuleContext(Egrep_op24Context.class,0);
		}
		public Egrep_op25Context egrep_op25() {
			return getRuleContext(Egrep_op25Context.class,0);
		}
		public Egrep_op26Context egrep_op26() {
			return getRuleContext(Egrep_op26Context.class,0);
		}
		public Egrep_op27Context egrep_op27() {
			return getRuleContext(Egrep_op27Context.class,0);
		}
		public Egrep_op28Context egrep_op28() {
			return getRuleContext(Egrep_op28Context.class,0);
		}
		public Egrep_op29Context egrep_op29() {
			return getRuleContext(Egrep_op29Context.class,0);
		}
		public Egrep_op30Context egrep_op30() {
			return getRuleContext(Egrep_op30Context.class,0);
		}
		public Egrep_op31Context egrep_op31() {
			return getRuleContext(Egrep_op31Context.class,0);
		}
		public Egrep_op32Context egrep_op32() {
			return getRuleContext(Egrep_op32Context.class,0);
		}
		public Egrep_op33Context egrep_op33() {
			return getRuleContext(Egrep_op33Context.class,0);
		}
		public Egrep_op34Context egrep_op34() {
			return getRuleContext(Egrep_op34Context.class,0);
		}
		public Egrep_op35Context egrep_op35() {
			return getRuleContext(Egrep_op35Context.class,0);
		}
		public Egrep_op36Context egrep_op36() {
			return getRuleContext(Egrep_op36Context.class,0);
		}
		public Egrep_op37Context egrep_op37() {
			return getRuleContext(Egrep_op37Context.class,0);
		}
		public Egrep_op38Context egrep_op38() {
			return getRuleContext(Egrep_op38Context.class,0);
		}
		public Egrep_op39Context egrep_op39() {
			return getRuleContext(Egrep_op39Context.class,0);
		}
		public Egrep_op40Context egrep_op40() {
			return getRuleContext(Egrep_op40Context.class,0);
		}
		public Cp_op1Context cp_op1() {
			return getRuleContext(Cp_op1Context.class,0);
		}
		public Cp_op5Context cp_op5() {
			return getRuleContext(Cp_op5Context.class,0);
		}
		public Cp_op6Context cp_op6() {
			return getRuleContext(Cp_op6Context.class,0);
		}
		public Cp_op7Context cp_op7() {
			return getRuleContext(Cp_op7Context.class,0);
		}
		public Cp_op8Context cp_op8() {
			return getRuleContext(Cp_op8Context.class,0);
		}
		public Cp_op9Context cp_op9() {
			return getRuleContext(Cp_op9Context.class,0);
		}
		public Ls_op0Context ls_op0() {
			return getRuleContext(Ls_op0Context.class,0);
		}
		public Ls_op1Context ls_op1() {
			return getRuleContext(Ls_op1Context.class,0);
		}
		public Ls_op2Context ls_op2() {
			return getRuleContext(Ls_op2Context.class,0);
		}
		public Ls_op3Context ls_op3() {
			return getRuleContext(Ls_op3Context.class,0);
		}
		public Ls_op4Context ls_op4() {
			return getRuleContext(Ls_op4Context.class,0);
		}
		public Ls_op5Context ls_op5() {
			return getRuleContext(Ls_op5Context.class,0);
		}
		public Ls_op6Context ls_op6() {
			return getRuleContext(Ls_op6Context.class,0);
		}
		public Ls_op7Context ls_op7() {
			return getRuleContext(Ls_op7Context.class,0);
		}
		public Ls_op8Context ls_op8() {
			return getRuleContext(Ls_op8Context.class,0);
		}
		public Ls_op9Context ls_op9() {
			return getRuleContext(Ls_op9Context.class,0);
		}
		public Ls_op10Context ls_op10() {
			return getRuleContext(Ls_op10Context.class,0);
		}
		public Ls_op11Context ls_op11() {
			return getRuleContext(Ls_op11Context.class,0);
		}
		public Ls_op12Context ls_op12() {
			return getRuleContext(Ls_op12Context.class,0);
		}
		public Ls_op13Context ls_op13() {
			return getRuleContext(Ls_op13Context.class,0);
		}
		public Ls_op14Context ls_op14() {
			return getRuleContext(Ls_op14Context.class,0);
		}
		public Ls_op15Context ls_op15() {
			return getRuleContext(Ls_op15Context.class,0);
		}
		public Ls_op16Context ls_op16() {
			return getRuleContext(Ls_op16Context.class,0);
		}
		public Ls_op17Context ls_op17() {
			return getRuleContext(Ls_op17Context.class,0);
		}
		public Ls_op18Context ls_op18() {
			return getRuleContext(Ls_op18Context.class,0);
		}
		public Ls_op19Context ls_op19() {
			return getRuleContext(Ls_op19Context.class,0);
		}
		public Ls_op20Context ls_op20() {
			return getRuleContext(Ls_op20Context.class,0);
		}
		public Ls_op21Context ls_op21() {
			return getRuleContext(Ls_op21Context.class,0);
		}
		public Ls_op22Context ls_op22() {
			return getRuleContext(Ls_op22Context.class,0);
		}
		public Ls_op23Context ls_op23() {
			return getRuleContext(Ls_op23Context.class,0);
		}
		public Ls_op24Context ls_op24() {
			return getRuleContext(Ls_op24Context.class,0);
		}
		public Ls_op25Context ls_op25() {
			return getRuleContext(Ls_op25Context.class,0);
		}
		public Ls_op26Context ls_op26() {
			return getRuleContext(Ls_op26Context.class,0);
		}
		public Ls_op27Context ls_op27() {
			return getRuleContext(Ls_op27Context.class,0);
		}
		public Ls_op28Context ls_op28() {
			return getRuleContext(Ls_op28Context.class,0);
		}
		public Ls_op29Context ls_op29() {
			return getRuleContext(Ls_op29Context.class,0);
		}
		public Ls_op30Context ls_op30() {
			return getRuleContext(Ls_op30Context.class,0);
		}
		public Ls_op31Context ls_op31() {
			return getRuleContext(Ls_op31Context.class,0);
		}
		public Ls_op32Context ls_op32() {
			return getRuleContext(Ls_op32Context.class,0);
		}
		public Ls_op33Context ls_op33() {
			return getRuleContext(Ls_op33Context.class,0);
		}
		public Ls_op34Context ls_op34() {
			return getRuleContext(Ls_op34Context.class,0);
		}
		public Ls_op35Context ls_op35() {
			return getRuleContext(Ls_op35Context.class,0);
		}
		public Ls_op36Context ls_op36() {
			return getRuleContext(Ls_op36Context.class,0);
		}
		public Ls_op37Context ls_op37() {
			return getRuleContext(Ls_op37Context.class,0);
		}
		public Ls_op38Context ls_op38() {
			return getRuleContext(Ls_op38Context.class,0);
		}
		public Tar_op0Context tar_op0() {
			return getRuleContext(Tar_op0Context.class,0);
		}
		public Tar_op1Context tar_op1() {
			return getRuleContext(Tar_op1Context.class,0);
		}
		public Tar_op2Context tar_op2() {
			return getRuleContext(Tar_op2Context.class,0);
		}
		public Tar_op3Context tar_op3() {
			return getRuleContext(Tar_op3Context.class,0);
		}
		public Tar_op4Context tar_op4() {
			return getRuleContext(Tar_op4Context.class,0);
		}
		public Tar_op5Context tar_op5() {
			return getRuleContext(Tar_op5Context.class,0);
		}
		public Tar_op6Context tar_op6() {
			return getRuleContext(Tar_op6Context.class,0);
		}
		public Tar_op7Context tar_op7() {
			return getRuleContext(Tar_op7Context.class,0);
		}
		public Tar_op8Context tar_op8() {
			return getRuleContext(Tar_op8Context.class,0);
		}
		public Tar_op9Context tar_op9() {
			return getRuleContext(Tar_op9Context.class,0);
		}
		public Tar_op10Context tar_op10() {
			return getRuleContext(Tar_op10Context.class,0);
		}
		public Tar_op11Context tar_op11() {
			return getRuleContext(Tar_op11Context.class,0);
		}
		public Tar_op12Context tar_op12() {
			return getRuleContext(Tar_op12Context.class,0);
		}
		public Tar_op13Context tar_op13() {
			return getRuleContext(Tar_op13Context.class,0);
		}
		public Tar_op14Context tar_op14() {
			return getRuleContext(Tar_op14Context.class,0);
		}
		public Tar_op15Context tar_op15() {
			return getRuleContext(Tar_op15Context.class,0);
		}
		public Tar_op16Context tar_op16() {
			return getRuleContext(Tar_op16Context.class,0);
		}
		public Tar_op17Context tar_op17() {
			return getRuleContext(Tar_op17Context.class,0);
		}
		public Tar_op18Context tar_op18() {
			return getRuleContext(Tar_op18Context.class,0);
		}
		public Tar_op19Context tar_op19() {
			return getRuleContext(Tar_op19Context.class,0);
		}
		public Tar_op20Context tar_op20() {
			return getRuleContext(Tar_op20Context.class,0);
		}
		public Tar_op21Context tar_op21() {
			return getRuleContext(Tar_op21Context.class,0);
		}
		public Tar_op22Context tar_op22() {
			return getRuleContext(Tar_op22Context.class,0);
		}
		public Tar_op23Context tar_op23() {
			return getRuleContext(Tar_op23Context.class,0);
		}
		public Tar_op24Context tar_op24() {
			return getRuleContext(Tar_op24Context.class,0);
		}
		public Tar_op25Context tar_op25() {
			return getRuleContext(Tar_op25Context.class,0);
		}
		public Tar_op26Context tar_op26() {
			return getRuleContext(Tar_op26Context.class,0);
		}
		public Tar_op27Context tar_op27() {
			return getRuleContext(Tar_op27Context.class,0);
		}
		public Tar_op28Context tar_op28() {
			return getRuleContext(Tar_op28Context.class,0);
		}
		public Tar_op29Context tar_op29() {
			return getRuleContext(Tar_op29Context.class,0);
		}
		public Tar_op30Context tar_op30() {
			return getRuleContext(Tar_op30Context.class,0);
		}
		public Tar_op31Context tar_op31() {
			return getRuleContext(Tar_op31Context.class,0);
		}
		public Tar_op32Context tar_op32() {
			return getRuleContext(Tar_op32Context.class,0);
		}
		public Tar_op35Context tar_op35() {
			return getRuleContext(Tar_op35Context.class,0);
		}
		public Tar_op36Context tar_op36() {
			return getRuleContext(Tar_op36Context.class,0);
		}
		public Tar_op37Context tar_op37() {
			return getRuleContext(Tar_op37Context.class,0);
		}
		public Tar_op38Context tar_op38() {
			return getRuleContext(Tar_op38Context.class,0);
		}
		public Tar_op39Context tar_op39() {
			return getRuleContext(Tar_op39Context.class,0);
		}
		public Tar_op40Context tar_op40() {
			return getRuleContext(Tar_op40Context.class,0);
		}
		public Tar_op41Context tar_op41() {
			return getRuleContext(Tar_op41Context.class,0);
		}
		public Tar_op42Context tar_op42() {
			return getRuleContext(Tar_op42Context.class,0);
		}
		public Tar_op43Context tar_op43() {
			return getRuleContext(Tar_op43Context.class,0);
		}
		public Tar_op44Context tar_op44() {
			return getRuleContext(Tar_op44Context.class,0);
		}
		public Tar_op45Context tar_op45() {
			return getRuleContext(Tar_op45Context.class,0);
		}
		public Tar_op46Context tar_op46() {
			return getRuleContext(Tar_op46Context.class,0);
		}
		public Tar_op47Context tar_op47() {
			return getRuleContext(Tar_op47Context.class,0);
		}
		public Tar_op48Context tar_op48() {
			return getRuleContext(Tar_op48Context.class,0);
		}
		public Xargs_op0Context xargs_op0() {
			return getRuleContext(Xargs_op0Context.class,0);
		}
		public Xargs_op1Context xargs_op1() {
			return getRuleContext(Xargs_op1Context.class,0);
		}
		public Xargs_op2Context xargs_op2() {
			return getRuleContext(Xargs_op2Context.class,0);
		}
		public Xargs_op3Context xargs_op3() {
			return getRuleContext(Xargs_op3Context.class,0);
		}
		public Xargs_op4Context xargs_op4() {
			return getRuleContext(Xargs_op4Context.class,0);
		}
		public Xargs_op6Context xargs_op6() {
			return getRuleContext(Xargs_op6Context.class,0);
		}
		public Xargs_op7Context xargs_op7() {
			return getRuleContext(Xargs_op7Context.class,0);
		}
		public Xargs_op8Context xargs_op8() {
			return getRuleContext(Xargs_op8Context.class,0);
		}
		public Xargs_op10Context xargs_op10() {
			return getRuleContext(Xargs_op10Context.class,0);
		}
		public Xargs_op11Context xargs_op11() {
			return getRuleContext(Xargs_op11Context.class,0);
		}
		public Xargs_op12Context xargs_op12() {
			return getRuleContext(Xargs_op12Context.class,0);
		}
		public Xargs_op14Context xargs_op14() {
			return getRuleContext(Xargs_op14Context.class,0);
		}
		public Sed_op0Context sed_op0() {
			return getRuleContext(Sed_op0Context.class,0);
		}
		public Sed_op1Context sed_op1() {
			return getRuleContext(Sed_op1Context.class,0);
		}
		public Sed_op2Context sed_op2() {
			return getRuleContext(Sed_op2Context.class,0);
		}
		public Sed_op3Context sed_op3() {
			return getRuleContext(Sed_op3Context.class,0);
		}
		public Sed_op4Context sed_op4() {
			return getRuleContext(Sed_op4Context.class,0);
		}
		public Sed_op5Context sed_op5() {
			return getRuleContext(Sed_op5Context.class,0);
		}
		public Sed_op6Context sed_op6() {
			return getRuleContext(Sed_op6Context.class,0);
		}
		public Sed_op7Context sed_op7() {
			return getRuleContext(Sed_op7Context.class,0);
		}
		public Awk_op0Context awk_op0() {
			return getRuleContext(Awk_op0Context.class,0);
		}
		public Awk_op1Context awk_op1() {
			return getRuleContext(Awk_op1Context.class,0);
		}
		public Awk_op4Context awk_op4() {
			return getRuleContext(Awk_op4Context.class,0);
		}
		public Awk_op5Context awk_op5() {
			return getRuleContext(Awk_op5Context.class,0);
		}
		public Rm_op0Context rm_op0() {
			return getRuleContext(Rm_op0Context.class,0);
		}
		public Rm_op1Context rm_op1() {
			return getRuleContext(Rm_op1Context.class,0);
		}
		public Rm_op2Context rm_op2() {
			return getRuleContext(Rm_op2Context.class,0);
		}
		public Rm_op3Context rm_op3() {
			return getRuleContext(Rm_op3Context.class,0);
		}
		public Rm_op4Context rm_op4() {
			return getRuleContext(Rm_op4Context.class,0);
		}
		public Rm_op5Context rm_op5() {
			return getRuleContext(Rm_op5Context.class,0);
		}
		public Rm_op6Context rm_op6() {
			return getRuleContext(Rm_op6Context.class,0);
		}
		public Rm_op7Context rm_op7() {
			return getRuleContext(Rm_op7Context.class,0);
		}
		public Cd_op0Context cd_op0() {
			return getRuleContext(Cd_op0Context.class,0);
		}
		public Cd_op1Context cd_op1() {
			return getRuleContext(Cd_op1Context.class,0);
		}
		public Wc_op0Context wc_op0() {
			return getRuleContext(Wc_op0Context.class,0);
		}
		public Wc_op1Context wc_op1() {
			return getRuleContext(Wc_op1Context.class,0);
		}
		public Wc_op2Context wc_op2() {
			return getRuleContext(Wc_op2Context.class,0);
		}
		public Wc_op3Context wc_op3() {
			return getRuleContext(Wc_op3Context.class,0);
		}
		public Wc_op4Context wc_op4() {
			return getRuleContext(Wc_op4Context.class,0);
		}
		public Chmod_op0Context chmod_op0() {
			return getRuleContext(Chmod_op0Context.class,0);
		}
		public Chmod_op1Context chmod_op1() {
			return getRuleContext(Chmod_op1Context.class,0);
		}
		public Chmod_op3Context chmod_op3() {
			return getRuleContext(Chmod_op3Context.class,0);
		}
		public Chmod_op7Context chmod_op7() {
			return getRuleContext(Chmod_op7Context.class,0);
		}
		public Chmod_op8Context chmod_op8() {
			return getRuleContext(Chmod_op8Context.class,0);
		}
		public Chmod_op9Context chmod_op9() {
			return getRuleContext(Chmod_op9Context.class,0);
		}
		public Chmod_op10Context chmod_op10() {
			return getRuleContext(Chmod_op10Context.class,0);
		}
		public Chmod_op11Context chmod_op11() {
			return getRuleContext(Chmod_op11Context.class,0);
		}
		public Chown_op0Context chown_op0() {
			return getRuleContext(Chown_op0Context.class,0);
		}
		public Chown_op1Context chown_op1() {
			return getRuleContext(Chown_op1Context.class,0);
		}
		public Chown_op2Context chown_op2() {
			return getRuleContext(Chown_op2Context.class,0);
		}
		public Chown_op4Context chown_op4() {
			return getRuleContext(Chown_op4Context.class,0);
		}
		public Head_op2Context head_op2() {
			return getRuleContext(Head_op2Context.class,0);
		}
		public Head_op3Context head_op3() {
			return getRuleContext(Head_op3Context.class,0);
		}
		public Tail_op0Context tail_op0() {
			return getRuleContext(Tail_op0Context.class,0);
		}
		public Tail_op1Context tail_op1() {
			return getRuleContext(Tail_op1Context.class,0);
		}
		public Tail_op5Context tail_op5() {
			return getRuleContext(Tail_op5Context.class,0);
		}
		public Tail_op6Context tail_op6() {
			return getRuleContext(Tail_op6Context.class,0);
		}
		public Seq_op0Context seq_op0() {
			return getRuleContext(Seq_op0Context.class,0);
		}
		public Seq_op1Context seq_op1() {
			return getRuleContext(Seq_op1Context.class,0);
		}
		public Seq_op2Context seq_op2() {
			return getRuleContext(Seq_op2Context.class,0);
		}
		public Seq_op3Context seq_op3() {
			return getRuleContext(Seq_op3Context.class,0);
		}
		public Seq_op5Context seq_op5() {
			return getRuleContext(Seq_op5Context.class,0);
		}
		public Cat_op0Context cat_op0() {
			return getRuleContext(Cat_op0Context.class,0);
		}
		public Cat_op1Context cat_op1() {
			return getRuleContext(Cat_op1Context.class,0);
		}
		public Cat_op2Context cat_op2() {
			return getRuleContext(Cat_op2Context.class,0);
		}
		public Cat_op3Context cat_op3() {
			return getRuleContext(Cat_op3Context.class,0);
		}
		public Cat_op4Context cat_op4() {
			return getRuleContext(Cat_op4Context.class,0);
		}
		public Cat_op5Context cat_op5() {
			return getRuleContext(Cat_op5Context.class,0);
		}
		public Cat_op6Context cat_op6() {
			return getRuleContext(Cat_op6Context.class,0);
		}
		public Cat_op7Context cat_op7() {
			return getRuleContext(Cat_op7Context.class,0);
		}
		public Zip_op0Context zip_op0() {
			return getRuleContext(Zip_op0Context.class,0);
		}
		public Zip_op1Context zip_op1() {
			return getRuleContext(Zip_op1Context.class,0);
		}
		public Zip_op2Context zip_op2() {
			return getRuleContext(Zip_op2Context.class,0);
		}
		public Zip_op3Context zip_op3() {
			return getRuleContext(Zip_op3Context.class,0);
		}
		public Zip_op4Context zip_op4() {
			return getRuleContext(Zip_op4Context.class,0);
		}
		public Zip_op5Context zip_op5() {
			return getRuleContext(Zip_op5Context.class,0);
		}
		public Zip_op6Context zip_op6() {
			return getRuleContext(Zip_op6Context.class,0);
		}
		public Zip_op7Context zip_op7() {
			return getRuleContext(Zip_op7Context.class,0);
		}
		public Zip_op8Context zip_op8() {
			return getRuleContext(Zip_op8Context.class,0);
		}
		public Zip_op9Context zip_op9() {
			return getRuleContext(Zip_op9Context.class,0);
		}
		public Zip_op10Context zip_op10() {
			return getRuleContext(Zip_op10Context.class,0);
		}
		public Zip_op11Context zip_op11() {
			return getRuleContext(Zip_op11Context.class,0);
		}
		public Zip_op12Context zip_op12() {
			return getRuleContext(Zip_op12Context.class,0);
		}
		public Zip_op13Context zip_op13() {
			return getRuleContext(Zip_op13Context.class,0);
		}
		public Zip_op14Context zip_op14() {
			return getRuleContext(Zip_op14Context.class,0);
		}
		public Zip_op15Context zip_op15() {
			return getRuleContext(Zip_op15Context.class,0);
		}
		public Zip_op16Context zip_op16() {
			return getRuleContext(Zip_op16Context.class,0);
		}
		public Zip_op17Context zip_op17() {
			return getRuleContext(Zip_op17Context.class,0);
		}
		public Zip_op18Context zip_op18() {
			return getRuleContext(Zip_op18Context.class,0);
		}
		public Zip_op19Context zip_op19() {
			return getRuleContext(Zip_op19Context.class,0);
		}
		public Zip_op20Context zip_op20() {
			return getRuleContext(Zip_op20Context.class,0);
		}
		public Zip_op21Context zip_op21() {
			return getRuleContext(Zip_op21Context.class,0);
		}
		public Zip_op22Context zip_op22() {
			return getRuleContext(Zip_op22Context.class,0);
		}
		public Zip_op23Context zip_op23() {
			return getRuleContext(Zip_op23Context.class,0);
		}
		public Zip_op24Context zip_op24() {
			return getRuleContext(Zip_op24Context.class,0);
		}
		public Zip_op25Context zip_op25() {
			return getRuleContext(Zip_op25Context.class,0);
		}
		public Zip_op26Context zip_op26() {
			return getRuleContext(Zip_op26Context.class,0);
		}
		public Zip_op27Context zip_op27() {
			return getRuleContext(Zip_op27Context.class,0);
		}
		public Zip_op28Context zip_op28() {
			return getRuleContext(Zip_op28Context.class,0);
		}
		public Zip_op29Context zip_op29() {
			return getRuleContext(Zip_op29Context.class,0);
		}
		public Zip_op30Context zip_op30() {
			return getRuleContext(Zip_op30Context.class,0);
		}
		public Zip_op31Context zip_op31() {
			return getRuleContext(Zip_op31Context.class,0);
		}
		public Zip_op32Context zip_op32() {
			return getRuleContext(Zip_op32Context.class,0);
		}
		public Zip_op33Context zip_op33() {
			return getRuleContext(Zip_op33Context.class,0);
		}
		public Zip_op34Context zip_op34() {
			return getRuleContext(Zip_op34Context.class,0);
		}
		public Zip_op35Context zip_op35() {
			return getRuleContext(Zip_op35Context.class,0);
		}
		public Zip_op36Context zip_op36() {
			return getRuleContext(Zip_op36Context.class,0);
		}
		public Zip_op37Context zip_op37() {
			return getRuleContext(Zip_op37Context.class,0);
		}
		public Zip_op39Context zip_op39() {
			return getRuleContext(Zip_op39Context.class,0);
		}
		public Zip_op40Context zip_op40() {
			return getRuleContext(Zip_op40Context.class,0);
		}
		public Unzip_op0Context unzip_op0() {
			return getRuleContext(Unzip_op0Context.class,0);
		}
		public Unzip_op1Context unzip_op1() {
			return getRuleContext(Unzip_op1Context.class,0);
		}
		public Unzip_op2Context unzip_op2() {
			return getRuleContext(Unzip_op2Context.class,0);
		}
		public Unzip_op3Context unzip_op3() {
			return getRuleContext(Unzip_op3Context.class,0);
		}
		public Unzip_op4Context unzip_op4() {
			return getRuleContext(Unzip_op4Context.class,0);
		}
		public Unzip_op5Context unzip_op5() {
			return getRuleContext(Unzip_op5Context.class,0);
		}
		public Unzip_op6Context unzip_op6() {
			return getRuleContext(Unzip_op6Context.class,0);
		}
		public Unzip_op7Context unzip_op7() {
			return getRuleContext(Unzip_op7Context.class,0);
		}
		public Unzip_op8Context unzip_op8() {
			return getRuleContext(Unzip_op8Context.class,0);
		}
		public Unzip_op9Context unzip_op9() {
			return getRuleContext(Unzip_op9Context.class,0);
		}
		public Unzip_op10Context unzip_op10() {
			return getRuleContext(Unzip_op10Context.class,0);
		}
		public Unzip_op11Context unzip_op11() {
			return getRuleContext(Unzip_op11Context.class,0);
		}
		public Unzip_op12Context unzip_op12() {
			return getRuleContext(Unzip_op12Context.class,0);
		}
		public Unzip_op13Context unzip_op13() {
			return getRuleContext(Unzip_op13Context.class,0);
		}
		public Unzip_op14Context unzip_op14() {
			return getRuleContext(Unzip_op14Context.class,0);
		}
		public Unzip_op15Context unzip_op15() {
			return getRuleContext(Unzip_op15Context.class,0);
		}
		public Unzip_op16Context unzip_op16() {
			return getRuleContext(Unzip_op16Context.class,0);
		}
		public Unzip_op17Context unzip_op17() {
			return getRuleContext(Unzip_op17Context.class,0);
		}
		public Unzip_op18Context unzip_op18() {
			return getRuleContext(Unzip_op18Context.class,0);
		}
		public Unzip_op19Context unzip_op19() {
			return getRuleContext(Unzip_op19Context.class,0);
		}
		public Unzip_op20Context unzip_op20() {
			return getRuleContext(Unzip_op20Context.class,0);
		}
		public Unzip_op21Context unzip_op21() {
			return getRuleContext(Unzip_op21Context.class,0);
		}
		public Unzip_op22Context unzip_op22() {
			return getRuleContext(Unzip_op22Context.class,0);
		}
		public Unzip_op23Context unzip_op23() {
			return getRuleContext(Unzip_op23Context.class,0);
		}
		public Unzip_op24Context unzip_op24() {
			return getRuleContext(Unzip_op24Context.class,0);
		}
		public Unzip_op25Context unzip_op25() {
			return getRuleContext(Unzip_op25Context.class,0);
		}
		public Unzip_op26Context unzip_op26() {
			return getRuleContext(Unzip_op26Context.class,0);
		}
		public Du_op0Context du_op0() {
			return getRuleContext(Du_op0Context.class,0);
		}
		public Du_op2Context du_op2() {
			return getRuleContext(Du_op2Context.class,0);
		}
		public Du_op3Context du_op3() {
			return getRuleContext(Du_op3Context.class,0);
		}
		public Du_op4Context du_op4() {
			return getRuleContext(Du_op4Context.class,0);
		}
		public Du_op5Context du_op5() {
			return getRuleContext(Du_op5Context.class,0);
		}
		public Du_op6Context du_op6() {
			return getRuleContext(Du_op6Context.class,0);
		}
		public Du_op7Context du_op7() {
			return getRuleContext(Du_op7Context.class,0);
		}
		public Echo_op0Context echo_op0() {
			return getRuleContext(Echo_op0Context.class,0);
		}
		public Echo_op1Context echo_op1() {
			return getRuleContext(Echo_op1Context.class,0);
		}
		public Diff_op0Context diff_op0() {
			return getRuleContext(Diff_op0Context.class,0);
		}
		public Comm_op0Context comm_op0() {
			return getRuleContext(Comm_op0Context.class,0);
		}
		public Comm_op1Context comm_op1() {
			return getRuleContext(Comm_op1Context.class,0);
		}
		public Comm_op2Context comm_op2() {
			return getRuleContext(Comm_op2Context.class,0);
		}
		public Comm_op3Context comm_op3() {
			return getRuleContext(Comm_op3Context.class,0);
		}
		public Sh_op0Context sh_op0() {
			return getRuleContext(Sh_op0Context.class,0);
		}
		public Sh_op1Context sh_op1() {
			return getRuleContext(Sh_op1Context.class,0);
		}
		public CommandContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_command; }
	}

	public final CommandContext command() throws RecognitionException {
		CommandContext _localctx = new CommandContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_command);
		int _la;
		try {
			int _alt;
			setState(2982);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,658,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(920);
				match(T__0);
				setState(922);
				_la = _input.LA(1);
				if (((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) {
					{
					setState(921);
					find_op0();
					}
				}

				setState(925);
				_la = _input.LA(1);
				if (_la==T__91) {
					{
					setState(924);
					find_op1();
					}
				}

				setState(928);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(927);
					find_op2();
					}
				}

				setState(931);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(930);
					find_op3();
					}
				}

				setState(934);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(933);
					find_op4();
					}
				}

				setState(937);
				_la = _input.LA(1);
				if (_la==T__13) {
					{
					setState(936);
					find_op5();
					}
				}

				setState(940);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(939);
					find_op6();
					}
				}

				setState(943); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(942);
					((CommandContext)_localctx).File = match(STRING);
					}
					}
					setState(945); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==STRING );
				setState(948);
				_la = _input.LA(1);
				if (_la==T__69) {
					{
					setState(947);
					find_op7();
					}
				}

				setState(951);
				_la = _input.LA(1);
				if (_la==T__137) {
					{
					setState(950);
					find_op8();
					}
				}

				setState(954);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,10,_ctx) ) {
				case 1:
					{
					setState(953);
					find_op9();
					}
					break;
				}
				setState(957);
				_la = _input.LA(1);
				if (_la==T__134) {
					{
					setState(956);
					find_op10();
					}
				}

				setState(960);
				_la = _input.LA(1);
				if (_la==T__144) {
					{
					setState(959);
					find_op11();
					}
				}

				setState(963);
				_la = _input.LA(1);
				if (_la==T__96) {
					{
					setState(962);
					find_op12();
					}
				}

				setState(966);
				_la = _input.LA(1);
				if (_la==T__98) {
					{
					setState(965);
					find_op13();
					}
				}

				setState(969);
				_la = _input.LA(1);
				if (_la==T__174) {
					{
					setState(968);
					find_op14();
					}
				}

				setState(972);
				_la = _input.LA(1);
				if (_la==T__44) {
					{
					setState(971);
					find_op15();
					}
				}

				setState(975);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,17,_ctx) ) {
				case 1:
					{
					setState(974);
					find_op16();
					}
					break;
				}
				setState(978);
				_la = _input.LA(1);
				if (_la==T__158) {
					{
					setState(977);
					find_op17();
					}
				}

				setState(981);
				_la = _input.LA(1);
				if (_la==T__166) {
					{
					setState(980);
					find_op18();
					}
				}

				setState(984);
				_la = _input.LA(1);
				if (_la==T__167) {
					{
					setState(983);
					find_op19();
					}
				}

				setState(987);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,21,_ctx) ) {
				case 1:
					{
					setState(986);
					find_op3();
					}
					break;
				}
				setState(990);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(989);
					find_op3();
					}
				}

				setState(993);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,23,_ctx) ) {
				case 1:
					{
					setState(992);
					find_op20();
					}
					break;
				}
				setState(996);
				_la = _input.LA(1);
				if (_la==T__116) {
					{
					setState(995);
					find_op21();
					}
				}

				setState(999);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(998);
					find_op4();
					}
				}

				setState(1002);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,26,_ctx) ) {
				case 1:
					{
					setState(1001);
					find_op22();
					}
					break;
				}
				setState(1005);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(1004);
					find_op20();
					}
				}

				setState(1008);
				_la = _input.LA(1);
				if (_la==T__10) {
					{
					setState(1007);
					find_op23();
					}
				}

				setState(1011);
				_la = _input.LA(1);
				if (_la==T__12) {
					{
					setState(1010);
					find_op22();
					}
				}

				setState(1014);
				_la = _input.LA(1);
				if (_la==T__76) {
					{
					setState(1013);
					find_op24();
					}
				}

				setState(1017);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,31,_ctx) ) {
				case 1:
					{
					setState(1016);
					find_op25();
					}
					break;
				}
				setState(1020);
				_la = _input.LA(1);
				if (_la==T__80) {
					{
					setState(1019);
					find_op26();
					}
				}

				setState(1023);
				_la = _input.LA(1);
				if (_la==T__66) {
					{
					setState(1022);
					find_op27();
					}
				}

				setState(1026);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,34,_ctx) ) {
				case 1:
					{
					setState(1025);
					find_op29();
					}
					break;
				}
				setState(1029);
				_la = _input.LA(1);
				if (_la==T__176) {
					{
					setState(1028);
					find_op30();
					}
				}

				setState(1032);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,36,_ctx) ) {
				case 1:
					{
					setState(1031);
					find_op31();
					}
					break;
				}
				setState(1035);
				_la = _input.LA(1);
				if (_la==T__88) {
					{
					setState(1034);
					find_op32();
					}
				}

				setState(1038);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,38,_ctx) ) {
				case 1:
					{
					setState(1037);
					find_op33();
					}
					break;
				}
				setState(1041);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,39,_ctx) ) {
				case 1:
					{
					setState(1040);
					find_op34();
					}
					break;
				}
				setState(1044);
				_la = _input.LA(1);
				if (_la==T__117) {
					{
					setState(1043);
					find_op35();
					}
				}

				setState(1047);
				_la = _input.LA(1);
				if (_la==T__68) {
					{
					setState(1046);
					find_op36();
					}
				}

				setState(1050);
				_la = _input.LA(1);
				if (_la==T__122) {
					{
					setState(1049);
					find_op37();
					}
				}

				setState(1053);
				_la = _input.LA(1);
				if (_la==T__46) {
					{
					setState(1052);
					find_op38();
					}
				}

				setState(1056);
				_la = _input.LA(1);
				if (_la==T__165) {
					{
					setState(1055);
					find_op39();
					}
				}

				setState(1059);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,45,_ctx) ) {
				case 1:
					{
					setState(1058);
					find_op40();
					}
					break;
				}
				setState(1062);
				_la = _input.LA(1);
				if (_la==T__142) {
					{
					setState(1061);
					find_op40();
					}
				}

				setState(1065);
				_la = _input.LA(1);
				if (_la==T__109) {
					{
					setState(1064);
					find_op41();
					}
				}

				setState(1068);
				_la = _input.LA(1);
				if (_la==T__99) {
					{
					setState(1067);
					find_op42();
					}
				}

				setState(1071);
				_la = _input.LA(1);
				if (_la==T__138) {
					{
					setState(1070);
					find_op43();
					}
				}

				setState(1074);
				_la = _input.LA(1);
				if (_la==T__129) {
					{
					setState(1073);
					find_op44();
					}
				}

				setState(1077);
				_la = _input.LA(1);
				if (_la==T__65) {
					{
					setState(1076);
					find_op45();
					}
				}

				setState(1080);
				_la = _input.LA(1);
				if (_la==T__173) {
					{
					setState(1079);
					find_op46();
					}
				}

				setState(1083);
				_la = _input.LA(1);
				if (_la==T__125) {
					{
					setState(1082);
					find_op47();
					}
				}

				setState(1086);
				_la = _input.LA(1);
				if (_la==T__143) {
					{
					setState(1085);
					find_op48();
					}
				}

				setState(1089);
				_la = _input.LA(1);
				if (_la==T__132) {
					{
					setState(1088);
					find_op49();
					}
				}

				setState(1092);
				_la = _input.LA(1);
				if (_la==T__141) {
					{
					setState(1091);
					find_op50();
					}
				}

				setState(1095);
				_la = _input.LA(1);
				if (_la==T__45) {
					{
					setState(1094);
					find_op51();
					}
				}

				setState(1098);
				_la = _input.LA(1);
				if (_la==T__130) {
					{
					setState(1097);
					find_op52();
					}
				}

				setState(1101);
				_la = _input.LA(1);
				if (_la==T__160) {
					{
					setState(1100);
					find_op53();
					}
				}

				setState(1104);
				_la = _input.LA(1);
				if (_la==T__136) {
					{
					setState(1103);
					find_op54();
					}
				}

				setState(1107);
				_la = _input.LA(1);
				if (_la==T__59) {
					{
					setState(1106);
					find_op55();
					}
				}

				setState(1110);
				_la = _input.LA(1);
				if (_la==T__118) {
					{
					setState(1109);
					find_op56();
					}
				}

				setState(1113);
				_la = _input.LA(1);
				if (_la==T__106) {
					{
					setState(1112);
					find_op57();
					}
				}

				setState(1116);
				_la = _input.LA(1);
				if (_la==T__121) {
					{
					setState(1115);
					find_op58();
					}
				}

				setState(1119);
				_la = _input.LA(1);
				if (_la==T__155) {
					{
					setState(1118);
					find_op59();
					}
				}

				setState(1122);
				_la = _input.LA(1);
				if (_la==T__163) {
					{
					setState(1121);
					find_op60();
					}
				}

				setState(1125);
				_la = _input.LA(1);
				if (_la==T__150) {
					{
					setState(1124);
					find_op61();
					}
				}

				setState(1128);
				_la = _input.LA(1);
				if (_la==T__175) {
					{
					setState(1127);
					find_op62();
					}
				}

				setState(1131);
				_la = _input.LA(1);
				if (_la==T__72) {
					{
					setState(1130);
					find_op63();
					}
				}

				setState(1134);
				_la = _input.LA(1);
				if (_la==T__140) {
					{
					setState(1133);
					find_op64();
					}
				}

				setState(1137);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,71,_ctx) ) {
				case 1:
					{
					setState(1136);
					find_op65();
					}
					break;
				}
				setState(1140);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,72,_ctx) ) {
				case 1:
					{
					setState(1139);
					find_op66();
					}
					break;
				}
				setState(1143);
				_la = _input.LA(1);
				if (_la==T__92) {
					{
					setState(1142);
					find_op67();
					}
				}

				setState(1146);
				_la = _input.LA(1);
				if (_la==T__128) {
					{
					setState(1145);
					find_op68();
					}
				}

				setState(1149);
				_la = _input.LA(1);
				if (_la==T__58) {
					{
					setState(1148);
					find_op69();
					}
				}

				setState(1152);
				_la = _input.LA(1);
				if (_la==T__147) {
					{
					setState(1151);
					find_op70();
					}
				}

				setState(1155);
				_la = _input.LA(1);
				if (_la==T__79) {
					{
					setState(1154);
					find_op71();
					}
				}

				setState(1158);
				_la = _input.LA(1);
				if (_la==T__108) {
					{
					setState(1157);
					find_op72();
					}
				}

				setState(1161);
				_la = _input.LA(1);
				if (_la==T__159) {
					{
					setState(1160);
					find_op73();
					}
				}

				setState(1164);
				_la = _input.LA(1);
				if (_la==T__102) {
					{
					setState(1163);
					find_op74();
					}
				}

				setState(1167);
				_la = _input.LA(1);
				if (_la==T__101) {
					{
					setState(1166);
					find_op75();
					}
				}

				setState(1170);
				_la = _input.LA(1);
				if (_la==T__13) {
					{
					setState(1169);
					find_op76();
					}
				}

				setState(1173);
				_la = _input.LA(1);
				if (_la==T__145) {
					{
					setState(1172);
					find_op77();
					}
				}

				setState(1176);
				_la = _input.LA(1);
				if (_la==T__172) {
					{
					setState(1175);
					find_op78();
					}
				}

				setState(1179);
				_la = _input.LA(1);
				if (_la==T__100) {
					{
					setState(1178);
					find_op79();
					}
				}

				setState(1182);
				_la = _input.LA(1);
				if (_la==T__169) {
					{
					setState(1181);
					find_op80();
					}
				}

				setState(1185);
				_la = _input.LA(1);
				if (_la==T__149) {
					{
					setState(1184);
					find_op81();
					}
				}

				setState(1188);
				_la = _input.LA(1);
				if (_la==T__67) {
					{
					setState(1187);
					find_op82();
					}
				}

				setState(1191);
				_la = _input.LA(1);
				if (_la==T__164) {
					{
					setState(1190);
					find_op83();
					}
				}

				setState(1194);
				_la = _input.LA(1);
				if (_la==T__97) {
					{
					setState(1193);
					find_op84();
					}
				}

				setState(1197);
				_la = _input.LA(1);
				if (_la==T__119) {
					{
					setState(1196);
					find_op85();
					}
				}

				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(1199);
				match(T__0);
				setState(1201);
				_la = _input.LA(1);
				if (((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) {
					{
					setState(1200);
					find_op0();
					}
				}

				setState(1204);
				_la = _input.LA(1);
				if (_la==T__91) {
					{
					setState(1203);
					find_op1();
					}
				}

				setState(1207);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(1206);
					find_op2();
					}
				}

				setState(1210);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(1209);
					find_op3();
					}
				}

				setState(1213);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(1212);
					find_op4();
					}
				}

				setState(1216);
				_la = _input.LA(1);
				if (_la==T__13) {
					{
					setState(1215);
					find_op5();
					}
				}

				setState(1218);
				match(T__1);
				setState(1219);
				((CommandContext)_localctx).File = match(STRING);
				setState(1221);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(1220);
					find_op86();
					}
				}

				setState(1224);
				_la = _input.LA(1);
				if (_la==T__69) {
					{
					setState(1223);
					find_op7();
					}
				}

				setState(1227);
				_la = _input.LA(1);
				if (_la==T__137) {
					{
					setState(1226);
					find_op8();
					}
				}

				setState(1230);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,101,_ctx) ) {
				case 1:
					{
					setState(1229);
					find_op9();
					}
					break;
				}
				setState(1233);
				_la = _input.LA(1);
				if (_la==T__134) {
					{
					setState(1232);
					find_op10();
					}
				}

				setState(1236);
				_la = _input.LA(1);
				if (_la==T__144) {
					{
					setState(1235);
					find_op11();
					}
				}

				setState(1239);
				_la = _input.LA(1);
				if (_la==T__96) {
					{
					setState(1238);
					find_op12();
					}
				}

				setState(1242);
				_la = _input.LA(1);
				if (_la==T__98) {
					{
					setState(1241);
					find_op13();
					}
				}

				setState(1245);
				_la = _input.LA(1);
				if (_la==T__174) {
					{
					setState(1244);
					find_op14();
					}
				}

				setState(1248);
				_la = _input.LA(1);
				if (_la==T__44) {
					{
					setState(1247);
					find_op15();
					}
				}

				setState(1251);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,108,_ctx) ) {
				case 1:
					{
					setState(1250);
					find_op16();
					}
					break;
				}
				setState(1254);
				_la = _input.LA(1);
				if (_la==T__158) {
					{
					setState(1253);
					find_op17();
					}
				}

				setState(1257);
				_la = _input.LA(1);
				if (_la==T__166) {
					{
					setState(1256);
					find_op18();
					}
				}

				setState(1260);
				_la = _input.LA(1);
				if (_la==T__167) {
					{
					setState(1259);
					find_op19();
					}
				}

				setState(1263);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,112,_ctx) ) {
				case 1:
					{
					setState(1262);
					find_op3();
					}
					break;
				}
				setState(1266);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(1265);
					find_op3();
					}
				}

				setState(1269);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,114,_ctx) ) {
				case 1:
					{
					setState(1268);
					find_op20();
					}
					break;
				}
				setState(1272);
				_la = _input.LA(1);
				if (_la==T__116) {
					{
					setState(1271);
					find_op21();
					}
				}

				setState(1275);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(1274);
					find_op4();
					}
				}

				setState(1278);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,117,_ctx) ) {
				case 1:
					{
					setState(1277);
					find_op22();
					}
					break;
				}
				setState(1281);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(1280);
					find_op20();
					}
				}

				setState(1284);
				_la = _input.LA(1);
				if (_la==T__10) {
					{
					setState(1283);
					find_op23();
					}
				}

				setState(1287);
				_la = _input.LA(1);
				if (_la==T__12) {
					{
					setState(1286);
					find_op22();
					}
				}

				setState(1290);
				_la = _input.LA(1);
				if (_la==T__76) {
					{
					setState(1289);
					find_op24();
					}
				}

				setState(1293);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,122,_ctx) ) {
				case 1:
					{
					setState(1292);
					find_op25();
					}
					break;
				}
				setState(1296);
				_la = _input.LA(1);
				if (_la==T__80) {
					{
					setState(1295);
					find_op26();
					}
				}

				setState(1299);
				_la = _input.LA(1);
				if (_la==T__66) {
					{
					setState(1298);
					find_op27();
					}
				}

				setState(1302);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,125,_ctx) ) {
				case 1:
					{
					setState(1301);
					find_op29();
					}
					break;
				}
				setState(1305);
				_la = _input.LA(1);
				if (_la==T__176) {
					{
					setState(1304);
					find_op30();
					}
				}

				setState(1308);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,127,_ctx) ) {
				case 1:
					{
					setState(1307);
					find_op31();
					}
					break;
				}
				setState(1311);
				_la = _input.LA(1);
				if (_la==T__88) {
					{
					setState(1310);
					find_op32();
					}
				}

				setState(1314);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,129,_ctx) ) {
				case 1:
					{
					setState(1313);
					find_op33();
					}
					break;
				}
				setState(1317);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,130,_ctx) ) {
				case 1:
					{
					setState(1316);
					find_op34();
					}
					break;
				}
				setState(1320);
				_la = _input.LA(1);
				if (_la==T__117) {
					{
					setState(1319);
					find_op35();
					}
				}

				setState(1323);
				_la = _input.LA(1);
				if (_la==T__68) {
					{
					setState(1322);
					find_op36();
					}
				}

				setState(1326);
				_la = _input.LA(1);
				if (_la==T__122) {
					{
					setState(1325);
					find_op37();
					}
				}

				setState(1329);
				_la = _input.LA(1);
				if (_la==T__46) {
					{
					setState(1328);
					find_op38();
					}
				}

				setState(1332);
				_la = _input.LA(1);
				if (_la==T__165) {
					{
					setState(1331);
					find_op39();
					}
				}

				setState(1335);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,136,_ctx) ) {
				case 1:
					{
					setState(1334);
					find_op40();
					}
					break;
				}
				setState(1338);
				_la = _input.LA(1);
				if (_la==T__142) {
					{
					setState(1337);
					find_op40();
					}
				}

				setState(1341);
				_la = _input.LA(1);
				if (_la==T__109) {
					{
					setState(1340);
					find_op41();
					}
				}

				setState(1344);
				_la = _input.LA(1);
				if (_la==T__99) {
					{
					setState(1343);
					find_op42();
					}
				}

				setState(1347);
				_la = _input.LA(1);
				if (_la==T__138) {
					{
					setState(1346);
					find_op43();
					}
				}

				setState(1350);
				_la = _input.LA(1);
				if (_la==T__129) {
					{
					setState(1349);
					find_op44();
					}
				}

				setState(1353);
				_la = _input.LA(1);
				if (_la==T__65) {
					{
					setState(1352);
					find_op45();
					}
				}

				setState(1356);
				_la = _input.LA(1);
				if (_la==T__173) {
					{
					setState(1355);
					find_op46();
					}
				}

				setState(1359);
				_la = _input.LA(1);
				if (_la==T__125) {
					{
					setState(1358);
					find_op47();
					}
				}

				setState(1362);
				_la = _input.LA(1);
				if (_la==T__143) {
					{
					setState(1361);
					find_op48();
					}
				}

				setState(1365);
				_la = _input.LA(1);
				if (_la==T__132) {
					{
					setState(1364);
					find_op49();
					}
				}

				setState(1368);
				_la = _input.LA(1);
				if (_la==T__141) {
					{
					setState(1367);
					find_op50();
					}
				}

				setState(1371);
				_la = _input.LA(1);
				if (_la==T__45) {
					{
					setState(1370);
					find_op51();
					}
				}

				setState(1374);
				_la = _input.LA(1);
				if (_la==T__130) {
					{
					setState(1373);
					find_op52();
					}
				}

				setState(1377);
				_la = _input.LA(1);
				if (_la==T__160) {
					{
					setState(1376);
					find_op53();
					}
				}

				setState(1380);
				_la = _input.LA(1);
				if (_la==T__136) {
					{
					setState(1379);
					find_op54();
					}
				}

				setState(1383);
				_la = _input.LA(1);
				if (_la==T__59) {
					{
					setState(1382);
					find_op55();
					}
				}

				setState(1386);
				_la = _input.LA(1);
				if (_la==T__118) {
					{
					setState(1385);
					find_op56();
					}
				}

				setState(1389);
				_la = _input.LA(1);
				if (_la==T__106) {
					{
					setState(1388);
					find_op57();
					}
				}

				setState(1392);
				_la = _input.LA(1);
				if (_la==T__121) {
					{
					setState(1391);
					find_op58();
					}
				}

				setState(1395);
				_la = _input.LA(1);
				if (_la==T__155) {
					{
					setState(1394);
					find_op59();
					}
				}

				setState(1398);
				_la = _input.LA(1);
				if (_la==T__163) {
					{
					setState(1397);
					find_op60();
					}
				}

				setState(1401);
				_la = _input.LA(1);
				if (_la==T__150) {
					{
					setState(1400);
					find_op61();
					}
				}

				setState(1404);
				_la = _input.LA(1);
				if (_la==T__175) {
					{
					setState(1403);
					find_op62();
					}
				}

				setState(1407);
				_la = _input.LA(1);
				if (_la==T__72) {
					{
					setState(1406);
					find_op63();
					}
				}

				setState(1410);
				_la = _input.LA(1);
				if (_la==T__140) {
					{
					setState(1409);
					find_op64();
					}
				}

				setState(1413);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,162,_ctx) ) {
				case 1:
					{
					setState(1412);
					find_op65();
					}
					break;
				}
				setState(1416);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,163,_ctx) ) {
				case 1:
					{
					setState(1415);
					find_op66();
					}
					break;
				}
				setState(1419);
				_la = _input.LA(1);
				if (_la==T__92) {
					{
					setState(1418);
					find_op67();
					}
				}

				setState(1422);
				_la = _input.LA(1);
				if (_la==T__128) {
					{
					setState(1421);
					find_op68();
					}
				}

				setState(1425);
				_la = _input.LA(1);
				if (_la==T__58) {
					{
					setState(1424);
					find_op69();
					}
				}

				setState(1428);
				_la = _input.LA(1);
				if (_la==T__147) {
					{
					setState(1427);
					find_op70();
					}
				}

				setState(1431);
				_la = _input.LA(1);
				if (_la==T__79) {
					{
					setState(1430);
					find_op71();
					}
				}

				setState(1434);
				_la = _input.LA(1);
				if (_la==T__108) {
					{
					setState(1433);
					find_op72();
					}
				}

				setState(1437);
				_la = _input.LA(1);
				if (_la==T__159) {
					{
					setState(1436);
					find_op73();
					}
				}

				setState(1440);
				_la = _input.LA(1);
				if (_la==T__102) {
					{
					setState(1439);
					find_op74();
					}
				}

				setState(1443);
				_la = _input.LA(1);
				if (_la==T__101) {
					{
					setState(1442);
					find_op75();
					}
				}

				setState(1446);
				_la = _input.LA(1);
				if (_la==T__13) {
					{
					setState(1445);
					find_op76();
					}
				}

				setState(1449);
				_la = _input.LA(1);
				if (_la==T__145) {
					{
					setState(1448);
					find_op77();
					}
				}

				setState(1452);
				_la = _input.LA(1);
				if (_la==T__172) {
					{
					setState(1451);
					find_op78();
					}
				}

				setState(1455);
				_la = _input.LA(1);
				if (_la==T__100) {
					{
					setState(1454);
					find_op79();
					}
				}

				setState(1458);
				_la = _input.LA(1);
				if (_la==T__169) {
					{
					setState(1457);
					find_op80();
					}
				}

				setState(1461);
				_la = _input.LA(1);
				if (_la==T__149) {
					{
					setState(1460);
					find_op81();
					}
				}

				setState(1464);
				_la = _input.LA(1);
				if (_la==T__67) {
					{
					setState(1463);
					find_op82();
					}
				}

				setState(1467);
				_la = _input.LA(1);
				if (_la==T__164) {
					{
					setState(1466);
					find_op83();
					}
				}

				setState(1470);
				_la = _input.LA(1);
				if (_la==T__97) {
					{
					setState(1469);
					find_op84();
					}
				}

				setState(1473);
				_la = _input.LA(1);
				if (_la==T__119) {
					{
					setState(1472);
					find_op85();
					}
				}

				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(1475);
				match(T__2);
				setState(1477);
				_la = _input.LA(1);
				if (_la==T__1 || _la==T__43 || _la==T__84) {
					{
					setState(1476);
					mv_op0();
					}
				}

				setState(1480);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(1479);
					mv_op1();
					}
				}

				setState(1482);
				((CommandContext)_localctx).File = match(STRING);
				setState(1483);
				((CommandContext)_localctx).File = match(STRING);
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(1484);
				match(T__2);
				setState(1486);
				_la = _input.LA(1);
				if (_la==T__1 || _la==T__43 || _la==T__84) {
					{
					setState(1485);
					mv_op0();
					}
				}

				setState(1489);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(1488);
					mv_op1();
					}
				}

				setState(1492); 
				_errHandler.sync(this);
				_alt = 1;
				do {
					switch (_alt) {
					case 1:
						{
						{
						setState(1491);
						((CommandContext)_localctx).File = match(STRING);
						}
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					setState(1494); 
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,187,_ctx);
				} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
				setState(1496);
				((CommandContext)_localctx).File = match(STRING);
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(1497);
				match(T__3);
				setState(1499);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(1498);
					sort_op0();
					}
				}

				setState(1502);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(1501);
					sort_op1();
					}
				}

				setState(1505);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(1504);
					sort_op2();
					}
				}

				setState(1508);
				_la = _input.LA(1);
				if (_la==T__37) {
					{
					setState(1507);
					sort_op3();
					}
				}

				setState(1511);
				_la = _input.LA(1);
				if (_la==T__84) {
					{
					setState(1510);
					sort_op4();
					}
				}

				setState(1514);
				_la = _input.LA(1);
				if (_la==T__42) {
					{
					setState(1513);
					sort_op5();
					}
				}

				setState(1517);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(1516);
					sort_op6();
					}
				}

				setState(1520);
				_la = _input.LA(1);
				if (_la==T__10) {
					{
					setState(1519);
					sort_op7();
					}
				}

				setState(1523);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(1522);
					sort_op8();
					}
				}

				setState(1526);
				_la = _input.LA(1);
				if (_la==T__64) {
					{
					setState(1525);
					sort_op9();
					}
				}

				setState(1529);
				_la = _input.LA(1);
				if (_la==T__36) {
					{
					setState(1528);
					sort_op10();
					}
				}

				setState(1532);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(1531);
					sort_op11();
					}
				}

				setState(1535);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(1534);
					sort_op12();
					}
				}

				setState(1538);
				_la = _input.LA(1);
				if (_la==T__55) {
					{
					setState(1537);
					sort_op13();
					}
				}

				setState(1541);
				_la = _input.LA(1);
				if (_la==T__12) {
					{
					setState(1540);
					sort_op14();
					}
				}

				setState(1544);
				_la = _input.LA(1);
				if (_la==T__47) {
					{
					setState(1543);
					sort_op15();
					}
				}

				setState(1547);
				_la = _input.LA(1);
				if (_la==T__11) {
					{
					setState(1546);
					sort_op16();
					}
				}

				setState(1550);
				_la = _input.LA(1);
				if (_la==T__127) {
					{
					setState(1549);
					sort_op17();
					}
				}

				setState(1553);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(1552);
					sort_op18();
					}
				}

				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(1555);
				match(T__4);
				setState(1557);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(1556);
					grep_op0();
					}
				}

				setState(1560);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(1559);
					grep_op1();
					}
				}

				setState(1563);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(1562);
					grep_op2();
					}
				}

				setState(1566);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(1565);
					grep_op3();
					}
				}

				setState(1569);
				_la = _input.LA(1);
				if (_la==T__139) {
					{
					setState(1568);
					grep_op4();
					}
				}

				setState(1572);
				_la = _input.LA(1);
				if (_la==T__91) {
					{
					setState(1571);
					grep_op5();
					}
				}

				setState(1575);
				_la = _input.LA(1);
				if (_la==T__52) {
					{
					setState(1574);
					grep_op6();
					}
				}

				setState(1578);
				_la = _input.LA(1);
				if (_la==T__86) {
					{
					setState(1577);
					grep_op7();
					}
				}

				setState(1581);
				_la = _input.LA(1);
				if (_la==T__82) {
					{
					setState(1580);
					grep_op8();
					}
				}

				setState(1584);
				_la = _input.LA(1);
				if (_la==T__94) {
					{
					setState(1583);
					grep_op9();
					}
				}

				setState(1587);
				_la = _input.LA(1);
				if (_la==T__103) {
					{
					setState(1586);
					grep_op10();
					}
				}

				setState(1590);
				_la = _input.LA(1);
				if (_la==T__84) {
					{
					setState(1589);
					grep_op11();
					}
				}

				setState(1593);
				_la = _input.LA(1);
				if (_la==T__61) {
					{
					setState(1592);
					grep_op12();
					}
				}

				setState(1596);
				_la = _input.LA(1);
				if (_la==T__83) {
					{
					setState(1595);
					grep_op13();
					}
				}

				setState(1599);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(1598);
					grep_op14();
					}
				}

				setState(1602);
				_la = _input.LA(1);
				if (_la==T__36) {
					{
					setState(1601);
					grep_op15();
					}
				}

				setState(1605);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(1604);
					grep_op16();
					}
				}

				setState(1608);
				_la = _input.LA(1);
				if (_la==T__133) {
					{
					setState(1607);
					grep_op17();
					}
				}

				setState(1611);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(1610);
					grep_op18();
					}
				}

				setState(1614);
				_la = _input.LA(1);
				if (_la==T__95) {
					{
					setState(1613);
					grep_op19();
					}
				}

				setState(1617);
				_la = _input.LA(1);
				if (_la==T__62) {
					{
					setState(1616);
					grep_op20();
					}
				}

				setState(1620);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(1619);
					grep_op21();
					}
				}

				setState(1623);
				_la = _input.LA(1);
				if (_la==T__55) {
					{
					setState(1622);
					grep_op22();
					}
				}

				setState(1626);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(1625);
					grep_op23();
					}
				}

				setState(1629);
				_la = _input.LA(1);
				if (_la==T__48) {
					{
					setState(1628);
					grep_op24();
					}
				}

				setState(1632);
				_la = _input.LA(1);
				if (_la==T__115) {
					{
					setState(1631);
					grep_op25();
					}
				}

				setState(1635);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(1634);
					grep_op26();
					}
				}

				setState(1638);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(1637);
					grep_op27();
					}
				}

				setState(1641);
				_la = _input.LA(1);
				if (_la==T__13) {
					{
					setState(1640);
					grep_op28();
					}
				}

				setState(1644);
				_la = _input.LA(1);
				if (_la==T__71) {
					{
					setState(1643);
					grep_op29();
					}
				}

				setState(1647);
				_la = _input.LA(1);
				if (_la==T__63) {
					{
					setState(1646);
					grep_op30();
					}
				}

				setState(1650);
				_la = _input.LA(1);
				if (_la==T__120) {
					{
					setState(1649);
					grep_op31();
					}
				}

				setState(1653);
				_la = _input.LA(1);
				if (_la==T__60) {
					{
					setState(1652);
					grep_op32();
					}
				}

				setState(1656);
				_la = _input.LA(1);
				if (_la==T__85) {
					{
					setState(1655);
					grep_op33();
					}
				}

				setState(1659);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(1658);
					grep_op34();
					}
				}

				setState(1662);
				_la = _input.LA(1);
				if (_la==T__87) {
					{
					setState(1661);
					grep_op35();
					}
				}

				setState(1665);
				_la = _input.LA(1);
				if (_la==T__75) {
					{
					setState(1664);
					grep_op36();
					}
				}

				setState(1668);
				_la = _input.LA(1);
				if (_la==T__110) {
					{
					setState(1667);
					grep_op37();
					}
				}

				setState(1671);
				_la = _input.LA(1);
				if (_la==T__135) {
					{
					setState(1670);
					grep_op38();
					}
				}

				setState(1674);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,246,_ctx) ) {
				case 1:
					{
					setState(1673);
					grep_op39();
					}
					break;
				}
				setState(1677);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(1676);
					grep_op40();
					}
				}

				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(1679);
				match(T__5);
				setState(1681);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(1680);
					egrep_op0();
					}
				}

				setState(1684);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(1683);
					egrep_op1();
					}
				}

				setState(1687);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(1686);
					egrep_op2();
					}
				}

				setState(1690);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(1689);
					egrep_op3();
					}
				}

				setState(1693);
				_la = _input.LA(1);
				if (_la==T__139) {
					{
					setState(1692);
					egrep_op4();
					}
				}

				setState(1696);
				_la = _input.LA(1);
				if (_la==T__91) {
					{
					setState(1695);
					egrep_op5();
					}
				}

				setState(1699);
				_la = _input.LA(1);
				if (_la==T__52) {
					{
					setState(1698);
					egrep_op6();
					}
				}

				setState(1702);
				_la = _input.LA(1);
				if (_la==T__86) {
					{
					setState(1701);
					egrep_op7();
					}
				}

				setState(1705);
				_la = _input.LA(1);
				if (_la==T__82) {
					{
					setState(1704);
					egrep_op8();
					}
				}

				setState(1708);
				_la = _input.LA(1);
				if (_la==T__94) {
					{
					setState(1707);
					egrep_op9();
					}
				}

				setState(1711);
				_la = _input.LA(1);
				if (_la==T__103) {
					{
					setState(1710);
					egrep_op10();
					}
				}

				setState(1714);
				_la = _input.LA(1);
				if (_la==T__84) {
					{
					setState(1713);
					egrep_op11();
					}
				}

				setState(1717);
				_la = _input.LA(1);
				if (_la==T__61) {
					{
					setState(1716);
					egrep_op12();
					}
				}

				setState(1720);
				_la = _input.LA(1);
				if (_la==T__83) {
					{
					setState(1719);
					egrep_op13();
					}
				}

				setState(1723);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(1722);
					egrep_op14();
					}
				}

				setState(1726);
				_la = _input.LA(1);
				if (_la==T__36) {
					{
					setState(1725);
					egrep_op15();
					}
				}

				setState(1729);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(1728);
					egrep_op16();
					}
				}

				setState(1732);
				_la = _input.LA(1);
				if (_la==T__133) {
					{
					setState(1731);
					egrep_op17();
					}
				}

				setState(1735);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(1734);
					egrep_op18();
					}
				}

				setState(1738);
				_la = _input.LA(1);
				if (_la==T__95) {
					{
					setState(1737);
					egrep_op19();
					}
				}

				setState(1741);
				_la = _input.LA(1);
				if (_la==T__62) {
					{
					setState(1740);
					egrep_op20();
					}
				}

				setState(1744);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(1743);
					egrep_op21();
					}
				}

				setState(1747);
				_la = _input.LA(1);
				if (_la==T__55) {
					{
					setState(1746);
					egrep_op22();
					}
				}

				setState(1750);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(1749);
					egrep_op23();
					}
				}

				setState(1753);
				_la = _input.LA(1);
				if (_la==T__48) {
					{
					setState(1752);
					egrep_op24();
					}
				}

				setState(1756);
				_la = _input.LA(1);
				if (_la==T__115) {
					{
					setState(1755);
					egrep_op25();
					}
				}

				setState(1759);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(1758);
					egrep_op26();
					}
				}

				setState(1762);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(1761);
					egrep_op27();
					}
				}

				setState(1765);
				_la = _input.LA(1);
				if (_la==T__13) {
					{
					setState(1764);
					egrep_op28();
					}
				}

				setState(1768);
				_la = _input.LA(1);
				if (_la==T__71) {
					{
					setState(1767);
					egrep_op29();
					}
				}

				setState(1771);
				_la = _input.LA(1);
				if (_la==T__63) {
					{
					setState(1770);
					egrep_op30();
					}
				}

				setState(1774);
				_la = _input.LA(1);
				if (_la==T__120) {
					{
					setState(1773);
					egrep_op31();
					}
				}

				setState(1777);
				_la = _input.LA(1);
				if (_la==T__60) {
					{
					setState(1776);
					egrep_op32();
					}
				}

				setState(1780);
				_la = _input.LA(1);
				if (_la==T__85) {
					{
					setState(1779);
					egrep_op33();
					}
				}

				setState(1783);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(1782);
					egrep_op34();
					}
				}

				setState(1786);
				_la = _input.LA(1);
				if (_la==T__87) {
					{
					setState(1785);
					egrep_op35();
					}
				}

				setState(1789);
				_la = _input.LA(1);
				if (_la==T__75) {
					{
					setState(1788);
					egrep_op36();
					}
				}

				setState(1792);
				_la = _input.LA(1);
				if (_la==T__110) {
					{
					setState(1791);
					egrep_op37();
					}
				}

				setState(1795);
				_la = _input.LA(1);
				if (_la==T__135) {
					{
					setState(1794);
					egrep_op38();
					}
				}

				setState(1798);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,287,_ctx) ) {
				case 1:
					{
					setState(1797);
					egrep_op39();
					}
					break;
				}
				setState(1801);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(1800);
					egrep_op40();
					}
				}

				}
				break;
			case 8:
				enterOuterAlt(_localctx, 8);
				{
				setState(1803);
				match(T__6);
				setState(1805);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(1804);
					cp_op1();
					}
				}

				setState(1808);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,290,_ctx) ) {
				case 1:
					{
					setState(1807);
					cp_op5();
					}
					break;
				}
				setState(1811);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(1810);
					cp_op6();
					}
				}

				setState(1814);
				_la = _input.LA(1);
				if (_la==T__95) {
					{
					setState(1813);
					cp_op7();
					}
				}

				setState(1817);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(1816);
					cp_op8();
					}
				}

				setState(1820);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(1819);
					cp_op9();
					}
				}

				setState(1822);
				((CommandContext)_localctx).File = match(STRING);
				setState(1823);
				((CommandContext)_localctx).File = match(STRING);
				}
				break;
			case 9:
				enterOuterAlt(_localctx, 9);
				{
				setState(1824);
				match(T__6);
				setState(1826);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(1825);
					cp_op1();
					}
				}

				setState(1829);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,296,_ctx) ) {
				case 1:
					{
					setState(1828);
					cp_op5();
					}
					break;
				}
				setState(1832);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(1831);
					cp_op6();
					}
				}

				setState(1835);
				_la = _input.LA(1);
				if (_la==T__95) {
					{
					setState(1834);
					cp_op7();
					}
				}

				setState(1838);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(1837);
					cp_op8();
					}
				}

				setState(1841);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(1840);
					cp_op9();
					}
				}

				setState(1844); 
				_errHandler.sync(this);
				_alt = 1;
				do {
					switch (_alt) {
					case 1:
						{
						{
						setState(1843);
						((CommandContext)_localctx).File = match(STRING);
						}
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					setState(1846); 
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,301,_ctx);
				} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
				setState(1848);
				((CommandContext)_localctx).File = match(STRING);
				}
				break;
			case 10:
				enterOuterAlt(_localctx, 10);
				{
				setState(1849);
				match(T__7);
				setState(1851);
				_la = _input.LA(1);
				if (_la==T__63) {
					{
					setState(1850);
					ls_op0();
					}
				}

				setState(1854);
				_la = _input.LA(1);
				if (_la==T__120) {
					{
					setState(1853);
					ls_op1();
					}
				}

				setState(1857);
				_la = _input.LA(1);
				if (_la==T__60) {
					{
					setState(1856);
					ls_op2();
					}
				}

				setState(1860);
				_la = _input.LA(1);
				if (_la==T__52) {
					{
					setState(1859);
					ls_op3();
					}
				}

				setState(1863);
				_la = _input.LA(1);
				if (_la==T__86) {
					{
					setState(1862);
					ls_op4();
					}
				}

				setState(1866);
				_la = _input.LA(1);
				if (_la==T__82) {
					{
					setState(1865);
					ls_op5();
					}
				}

				setState(1869);
				_la = _input.LA(1);
				if (_la==T__83) {
					{
					setState(1868);
					ls_op6();
					}
				}

				setState(1872);
				_la = _input.LA(1);
				if (_la==T__133) {
					{
					setState(1871);
					ls_op7();
					}
				}

				setState(1875);
				_la = _input.LA(1);
				if (_la==T__56) {
					{
					setState(1874);
					ls_op8();
					}
				}

				setState(1878);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(1877);
					ls_op9();
					}
				}

				setState(1881);
				_la = _input.LA(1);
				if (_la==T__55) {
					{
					setState(1880);
					ls_op10();
					}
				}

				setState(1884);
				_la = _input.LA(1);
				if (_la==T__47) {
					{
					setState(1883);
					ls_op11();
					}
				}

				setState(1887);
				_la = _input.LA(1);
				if (_la==T__48) {
					{
					setState(1886);
					ls_op12();
					}
				}

				setState(1890);
				_la = _input.LA(1);
				if (_la==T__111) {
					{
					setState(1889);
					ls_op13();
					}
				}

				setState(1893);
				_la = _input.LA(1);
				if (_la==T__123) {
					{
					setState(1892);
					ls_op14();
					}
				}

				setState(1896);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(1895);
					ls_op15();
					}
				}

				setState(1899);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(1898);
					ls_op16();
					}
				}

				setState(1902);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(1901);
					ls_op17();
					}
				}

				setState(1905);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(1904);
					ls_op18();
					}
				}

				setState(1908);
				_la = _input.LA(1);
				if (_la==T__85) {
					{
					setState(1907);
					ls_op19();
					}
				}

				setState(1911);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(1910);
					ls_op20();
					}
				}

				setState(1914);
				_la = _input.LA(1);
				if (_la==T__37) {
					{
					setState(1913);
					ls_op21();
					}
				}

				setState(1917);
				_la = _input.LA(1);
				if (_la==T__94) {
					{
					setState(1916);
					ls_op22();
					}
				}

				setState(1920);
				_la = _input.LA(1);
				if (_la==T__84) {
					{
					setState(1919);
					ls_op23();
					}
				}

				setState(1923);
				_la = _input.LA(1);
				if (_la==T__64) {
					{
					setState(1922);
					ls_op24();
					}
				}

				setState(1926);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(1925);
					ls_op25();
					}
				}

				setState(1929);
				_la = _input.LA(1);
				if (_la==T__36) {
					{
					setState(1928);
					ls_op26();
					}
				}

				setState(1932);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(1931);
					ls_op27();
					}
				}

				setState(1935);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(1934);
					ls_op28();
					}
				}

				setState(1938);
				_la = _input.LA(1);
				if (_la==T__95) {
					{
					setState(1937);
					ls_op29();
					}
				}

				setState(1941);
				_la = _input.LA(1);
				if (_la==T__62) {
					{
					setState(1940);
					ls_op30();
					}
				}

				setState(1944);
				_la = _input.LA(1);
				if (_la==T__10) {
					{
					setState(1943);
					ls_op31();
					}
				}

				setState(1947);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(1946);
					ls_op32();
					}
				}

				setState(1950);
				_la = _input.LA(1);
				if (_la==T__12) {
					{
					setState(1949);
					ls_op33();
					}
				}

				setState(1953);
				_la = _input.LA(1);
				if (_la==T__11) {
					{
					setState(1952);
					ls_op34();
					}
				}

				setState(1956);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(1955);
					ls_op35();
					}
				}

				setState(1959);
				_la = _input.LA(1);
				if (_la==T__13) {
					{
					setState(1958);
					ls_op36();
					}
				}

				setState(1962);
				_la = _input.LA(1);
				if (_la==T__153) {
					{
					setState(1961);
					ls_op37();
					}
				}

				setState(1965);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(1964);
					ls_op38();
					}
				}

				}
				break;
			case 11:
				enterOuterAlt(_localctx, 11);
				{
				setState(1967);
				match(T__8);
				setState(1968);
				match(T__9);
				setState(1970);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(1969);
					tar_op0();
					}
				}

				setState(1973);
				_la = _input.LA(1);
				if (_la==T__60) {
					{
					setState(1972);
					tar_op1();
					}
				}

				setState(1976);
				_la = _input.LA(1);
				if (_la==T__70) {
					{
					setState(1975);
					tar_op2();
					}
				}

				setState(1979);
				_la = _input.LA(1);
				if (_la==T__124) {
					{
					setState(1978);
					tar_op3();
					}
				}

				setState(1982);
				_la = _input.LA(1);
				if (_la==T__157) {
					{
					setState(1981);
					tar_op4();
					}
				}

				setState(1985);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(1984);
					tar_op5();
					}
				}

				setState(1988);
				_la = _input.LA(1);
				if (_la==T__82) {
					{
					setState(1987);
					tar_op6();
					}
				}

				setState(1991);
				_la = _input.LA(1);
				if (_la==T__94) {
					{
					setState(1990);
					tar_op7();
					}
				}

				setState(1994);
				_la = _input.LA(1);
				if (_la==T__103) {
					{
					setState(1993);
					tar_op8();
					}
				}

				setState(1997);
				_la = _input.LA(1);
				if (_la==T__126) {
					{
					setState(1996);
					tar_op9();
					}
				}

				setState(2000);
				_la = _input.LA(1);
				if (_la==T__53) {
					{
					setState(1999);
					tar_op10();
					}
				}

				setState(2003);
				_la = _input.LA(1);
				if (_la==T__83) {
					{
					setState(2002);
					tar_op11();
					}
				}

				setState(2006);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(2005);
					tar_op12();
					}
				}

				setState(2009);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(2008);
					tar_op13();
					}
				}

				setState(2012);
				_la = _input.LA(1);
				if (_la==T__156) {
					{
					setState(2011);
					tar_op14();
					}
				}

				setState(2015);
				_la = _input.LA(1);
				if (_la==T__171) {
					{
					setState(2014);
					tar_op15();
					}
				}

				setState(2018);
				_la = _input.LA(1);
				if (_la==T__162) {
					{
					setState(2017);
					tar_op16();
					}
				}

				setState(2021);
				_la = _input.LA(1);
				if (_la==T__104) {
					{
					setState(2020);
					tar_op17();
					}
				}

				setState(2024);
				_la = _input.LA(1);
				if (_la==T__113) {
					{
					setState(2023);
					tar_op18();
					}
				}

				setState(2027);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(2026);
					tar_op19();
					}
				}

				setState(2030);
				_la = _input.LA(1);
				if (_la==T__152) {
					{
					setState(2029);
					tar_op20();
					}
				}

				setState(2033);
				_la = _input.LA(1);
				if (_la==T__77) {
					{
					setState(2032);
					tar_op21();
					}
				}

				setState(2036);
				_la = _input.LA(1);
				if (_la==T__56) {
					{
					setState(2035);
					tar_op22();
					}
				}

				setState(2039);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(2038);
					tar_op23();
					}
				}

				setState(2042);
				_la = _input.LA(1);
				if (_la==T__47) {
					{
					setState(2041);
					tar_op24();
					}
				}

				setState(2045);
				_la = _input.LA(1);
				if (_la==T__154) {
					{
					setState(2044);
					tar_op25();
					}
				}

				setState(2048);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2047);
					tar_op26();
					}
				}

				setState(2051);
				_la = _input.LA(1);
				if (_la==T__161) {
					{
					setState(2050);
					tar_op27();
					}
				}

				setState(2054);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(2053);
					tar_op28();
					}
				}

				setState(2057);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(2056);
					tar_op29();
					}
				}

				setState(2060);
				_la = _input.LA(1);
				if (_la==T__116) {
					{
					setState(2059);
					tar_op30();
					}
				}

				setState(2063);
				_la = _input.LA(1);
				if (_la==T__127) {
					{
					setState(2062);
					tar_op31();
					}
				}

				setState(2066);
				_la = _input.LA(1);
				if (_la==T__71) {
					{
					setState(2065);
					tar_op32();
					}
				}

				setState(2069);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,374,_ctx) ) {
				case 1:
					{
					setState(2068);
					tar_op35();
					}
					break;
				}
				}
				break;
			case 12:
				enterOuterAlt(_localctx, 12);
				{
				setState(2071);
				match(T__8);
				setState(2072);
				match(T__10);
				setState(2073);
				match(T__1);
				setState(2074);
				((CommandContext)_localctx).File = match(STRING);
				setState(2076);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(2075);
					tar_op0();
					}
				}

				setState(2079);
				_la = _input.LA(1);
				if (_la==T__60) {
					{
					setState(2078);
					tar_op1();
					}
				}

				setState(2082);
				_la = _input.LA(1);
				if (_la==T__70) {
					{
					setState(2081);
					tar_op2();
					}
				}

				setState(2085);
				_la = _input.LA(1);
				if (_la==T__124) {
					{
					setState(2084);
					tar_op3();
					}
				}

				setState(2088);
				_la = _input.LA(1);
				if (_la==T__157) {
					{
					setState(2087);
					tar_op4();
					}
				}

				setState(2091);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2090);
					tar_op5();
					}
				}

				setState(2094);
				_la = _input.LA(1);
				if (_la==T__82) {
					{
					setState(2093);
					tar_op6();
					}
				}

				setState(2097);
				_la = _input.LA(1);
				if (_la==T__94) {
					{
					setState(2096);
					tar_op7();
					}
				}

				setState(2100);
				_la = _input.LA(1);
				if (_la==T__103) {
					{
					setState(2099);
					tar_op8();
					}
				}

				setState(2103);
				_la = _input.LA(1);
				if (_la==T__126) {
					{
					setState(2102);
					tar_op9();
					}
				}

				setState(2106);
				_la = _input.LA(1);
				if (_la==T__83) {
					{
					setState(2105);
					tar_op11();
					}
				}

				setState(2109);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(2108);
					tar_op12();
					}
				}

				setState(2112);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(2111);
					tar_op13();
					}
				}

				setState(2115);
				_la = _input.LA(1);
				if (_la==T__156) {
					{
					setState(2114);
					tar_op14();
					}
				}

				setState(2118);
				_la = _input.LA(1);
				if (_la==T__171) {
					{
					setState(2117);
					tar_op15();
					}
				}

				setState(2121);
				_la = _input.LA(1);
				if (_la==T__162) {
					{
					setState(2120);
					tar_op16();
					}
				}

				setState(2124);
				_la = _input.LA(1);
				if (_la==T__104) {
					{
					setState(2123);
					tar_op17();
					}
				}

				setState(2127);
				_la = _input.LA(1);
				if (_la==T__113) {
					{
					setState(2126);
					tar_op18();
					}
				}

				setState(2130);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(2129);
					tar_op19();
					}
				}

				setState(2133);
				_la = _input.LA(1);
				if (_la==T__152) {
					{
					setState(2132);
					tar_op20();
					}
				}

				setState(2136);
				_la = _input.LA(1);
				if (_la==T__77) {
					{
					setState(2135);
					tar_op21();
					}
				}

				setState(2139);
				_la = _input.LA(1);
				if (_la==T__56) {
					{
					setState(2138);
					tar_op22();
					}
				}

				setState(2142);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(2141);
					tar_op23();
					}
				}

				setState(2145);
				_la = _input.LA(1);
				if (_la==T__47) {
					{
					setState(2144);
					tar_op24();
					}
				}

				setState(2148);
				_la = _input.LA(1);
				if (_la==T__154) {
					{
					setState(2147);
					tar_op25();
					}
				}

				setState(2151);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2150);
					tar_op26();
					}
				}

				setState(2154);
				_la = _input.LA(1);
				if (_la==T__161) {
					{
					setState(2153);
					tar_op27();
					}
				}

				setState(2157);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(2156);
					tar_op28();
					}
				}

				setState(2160);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(2159);
					tar_op29();
					}
				}

				setState(2163);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,404,_ctx) ) {
				case 1:
					{
					setState(2162);
					tar_op35();
					}
					break;
				}
				}
				break;
			case 13:
				enterOuterAlt(_localctx, 13);
				{
				setState(2165);
				match(T__8);
				setState(2166);
				match(T__11);
				setState(2167);
				match(T__1);
				setState(2168);
				((CommandContext)_localctx).File = match(STRING);
				setState(2170);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(2169);
					tar_op0();
					}
				}

				setState(2173);
				_la = _input.LA(1);
				if (_la==T__60) {
					{
					setState(2172);
					tar_op1();
					}
				}

				setState(2176);
				_la = _input.LA(1);
				if (_la==T__124) {
					{
					setState(2175);
					tar_op3();
					}
				}

				setState(2179);
				_la = _input.LA(1);
				if (_la==T__157) {
					{
					setState(2178);
					tar_op36();
					}
				}

				setState(2182);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2181);
					tar_op5();
					}
				}

				setState(2185);
				_la = _input.LA(1);
				if (_la==T__103) {
					{
					setState(2184);
					tar_op8();
					}
				}

				setState(2188);
				_la = _input.LA(1);
				if (_la==T__126) {
					{
					setState(2187);
					tar_op9();
					}
				}

				setState(2191);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(2190);
					tar_op12();
					}
				}

				setState(2194);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(2193);
					tar_op13();
					}
				}

				setState(2197);
				_la = _input.LA(1);
				if (_la==T__156) {
					{
					setState(2196);
					tar_op14();
					}
				}

				setState(2200);
				_la = _input.LA(1);
				if (_la==T__171) {
					{
					setState(2199);
					tar_op15();
					}
				}

				setState(2203);
				_la = _input.LA(1);
				if (_la==T__162) {
					{
					setState(2202);
					tar_op16();
					}
				}

				setState(2206);
				_la = _input.LA(1);
				if (_la==T__104) {
					{
					setState(2205);
					tar_op17();
					}
				}

				setState(2209);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(2208);
					tar_op19();
					}
				}

				setState(2212);
				_la = _input.LA(1);
				if (_la==T__152) {
					{
					setState(2211);
					tar_op20();
					}
				}

				setState(2215);
				_la = _input.LA(1);
				if (_la==T__77) {
					{
					setState(2214);
					tar_op21();
					}
				}

				setState(2218);
				_la = _input.LA(1);
				if (_la==T__56) {
					{
					setState(2217);
					tar_op22();
					}
				}

				setState(2221);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(2220);
					tar_op23();
					}
				}

				setState(2224);
				_la = _input.LA(1);
				if (_la==T__47) {
					{
					setState(2223);
					tar_op24();
					}
				}

				setState(2227);
				_la = _input.LA(1);
				if (_la==T__154) {
					{
					setState(2226);
					tar_op25();
					}
				}

				setState(2230);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2229);
					tar_op26();
					}
				}

				setState(2233);
				_la = _input.LA(1);
				if (_la==T__161) {
					{
					setState(2232);
					tar_op27();
					}
				}

				setState(2236);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(2235);
					tar_op28();
					}
				}

				setState(2239);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(2238);
					tar_op29();
					}
				}

				setState(2242);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,429,_ctx) ) {
				case 1:
					{
					setState(2241);
					tar_op35();
					}
					break;
				}
				}
				break;
			case 14:
				enterOuterAlt(_localctx, 14);
				{
				setState(2244);
				match(T__8);
				setState(2245);
				match(T__12);
				setState(2247);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(2246);
					tar_op0();
					}
				}

				setState(2250);
				_la = _input.LA(1);
				if (_la==T__60) {
					{
					setState(2249);
					tar_op1();
					}
				}

				setState(2253);
				_la = _input.LA(1);
				if (_la==T__124) {
					{
					setState(2252);
					tar_op3();
					}
				}

				setState(2256);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2255);
					tar_op5();
					}
				}

				setState(2259);
				_la = _input.LA(1);
				if (_la==T__103) {
					{
					setState(2258);
					tar_op8();
					}
				}

				setState(2262);
				_la = _input.LA(1);
				if (_la==T__126) {
					{
					setState(2261);
					tar_op9();
					}
				}

				setState(2265);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(2264);
					tar_op12();
					}
				}

				setState(2268);
				_la = _input.LA(1);
				if (_la==T__133) {
					{
					setState(2267);
					tar_op37();
					}
				}

				setState(2271);
				_la = _input.LA(1);
				if (_la==T__77) {
					{
					setState(2270);
					tar_op21();
					}
				}

				setState(2274);
				_la = _input.LA(1);
				if (_la==T__56) {
					{
					setState(2273);
					tar_op22();
					}
				}

				setState(2277);
				_la = _input.LA(1);
				if (_la==T__62) {
					{
					setState(2276);
					tar_op38();
					}
				}

				setState(2280);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(2279);
					tar_op23();
					}
				}

				setState(2283);
				_la = _input.LA(1);
				if (_la==T__47) {
					{
					setState(2282);
					tar_op24();
					}
				}

				setState(2286);
				_la = _input.LA(1);
				if (_la==T__154) {
					{
					setState(2285);
					tar_op25();
					}
				}

				setState(2289);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2288);
					tar_op26();
					}
				}

				setState(2292);
				_la = _input.LA(1);
				if (_la==T__161) {
					{
					setState(2291);
					tar_op27();
					}
				}

				setState(2295);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(2294);
					tar_op28();
					}
				}

				setState(2298);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(2297);
					tar_op29();
					}
				}

				setState(2301);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2300);
					tar_op39();
					}
				}

				}
				break;
			case 15:
				enterOuterAlt(_localctx, 15);
				{
				setState(2303);
				match(T__8);
				setState(2304);
				match(T__13);
				setState(2306);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(2305);
					tar_op0();
					}
				}

				setState(2309);
				_la = _input.LA(1);
				if (_la==T__60) {
					{
					setState(2308);
					tar_op1();
					}
				}

				setState(2312);
				_la = _input.LA(1);
				if (_la==T__151) {
					{
					setState(2311);
					tar_op40();
					}
				}

				setState(2315);
				_la = _input.LA(1);
				if (_la==T__124) {
					{
					setState(2314);
					tar_op3();
					}
				}

				setState(2318);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2317);
					tar_op5();
					}
				}

				setState(2321);
				_la = _input.LA(1);
				if (_la==T__103) {
					{
					setState(2320);
					tar_op8();
					}
				}

				setState(2324);
				_la = _input.LA(1);
				if (_la==T__126) {
					{
					setState(2323);
					tar_op9();
					}
				}

				setState(2327);
				_la = _input.LA(1);
				if (_la==T__64) {
					{
					setState(2326);
					tar_op41();
					}
				}

				setState(2330);
				_la = _input.LA(1);
				if (_la==T__112) {
					{
					setState(2329);
					tar_op42();
					}
				}

				setState(2333);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(2332);
					tar_op12();
					}
				}

				setState(2336);
				_la = _input.LA(1);
				if (_la==T__36) {
					{
					setState(2335);
					tar_op43();
					}
				}

				setState(2339);
				_la = _input.LA(1);
				if (_la==T__90) {
					{
					setState(2338);
					tar_op44();
					}
				}

				setState(2342);
				_la = _input.LA(1);
				if (_la==T__133) {
					{
					setState(2341);
					tar_op37();
					}
				}

				setState(2345);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(2344);
					tar_op19();
					}
				}

				setState(2348);
				_la = _input.LA(1);
				if (_la==T__77) {
					{
					setState(2347);
					tar_op21();
					}
				}

				setState(2351);
				_la = _input.LA(1);
				if (_la==T__56) {
					{
					setState(2350);
					tar_op22();
					}
				}

				setState(2354);
				_la = _input.LA(1);
				if (_la==T__95) {
					{
					setState(2353);
					tar_op45();
					}
				}

				setState(2357);
				_la = _input.LA(1);
				if (_la==T__62) {
					{
					setState(2356);
					tar_op38();
					}
				}

				setState(2360);
				_la = _input.LA(1);
				if (_la==T__55) {
					{
					setState(2359);
					tar_op46();
					}
				}

				setState(2363);
				_la = _input.LA(1);
				if (_la==T__35) {
					{
					setState(2362);
					tar_op47();
					}
				}

				setState(2366);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(2365);
					tar_op23();
					}
				}

				setState(2369);
				_la = _input.LA(1);
				if (_la==T__47) {
					{
					setState(2368);
					tar_op24();
					}
				}

				setState(2372);
				_la = _input.LA(1);
				if (_la==T__48) {
					{
					setState(2371);
					tar_op48();
					}
				}

				setState(2375);
				_la = _input.LA(1);
				if (_la==T__154) {
					{
					setState(2374);
					tar_op25();
					}
				}

				setState(2378);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2377);
					tar_op26();
					}
				}

				setState(2381);
				_la = _input.LA(1);
				if (_la==T__161) {
					{
					setState(2380);
					tar_op27();
					}
				}

				setState(2384);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(2383);
					tar_op28();
					}
				}

				setState(2387);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(2386);
					tar_op29();
					}
				}

				setState(2390);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2389);
					tar_op39();
					}
				}

				}
				break;
			case 16:
				enterOuterAlt(_localctx, 16);
				{
				setState(2392);
				match(T__14);
				setState(2394);
				_la = _input.LA(1);
				if (_la==T__148) {
					{
					setState(2393);
					xargs_op0();
					}
				}

				setState(2397);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(2396);
					xargs_op1();
					}
				}

				setState(2400);
				_la = _input.LA(1);
				if (_la==T__95) {
					{
					setState(2399);
					xargs_op2();
					}
				}

				setState(2403);
				_la = _input.LA(1);
				if (_la==T__12) {
					{
					setState(2402);
					xargs_op3();
					}
				}

				setState(2406);
				_la = _input.LA(1);
				if (_la==T__91) {
					{
					setState(2405);
					xargs_op4();
					}
				}

				setState(2409);
				_la = _input.LA(1);
				if (_la==T__103) {
					{
					setState(2408);
					xargs_op6();
					}
				}

				setState(2412);
				_la = _input.LA(1);
				if (_la==T__61) {
					{
					setState(2411);
					xargs_op7();
					}
				}

				setState(2415);
				_la = _input.LA(1);
				if (_la==T__83) {
					{
					setState(2414);
					xargs_op8();
					}
				}

				setState(2418);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(2417);
					xargs_op10();
					}
				}

				setState(2421);
				_la = _input.LA(1);
				if (_la==T__56) {
					{
					setState(2420);
					xargs_op11();
					}
				}

				setState(2424);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(2423);
					xargs_op12();
					}
				}

				setState(2427);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2426);
					xargs_op14();
					}
				}

				}
				break;
			case 17:
				enterOuterAlt(_localctx, 17);
				{
				setState(2429);
				match(T__15);
				setState(2431);
				_la = _input.LA(1);
				if (_la==T__91) {
					{
					setState(2430);
					sed_op0();
					}
				}

				setState(2434);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(2433);
					sed_op1();
					}
				}

				setState(2437);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(2436);
					sed_op2();
					}
				}

				setState(2440);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(2439);
					sed_op3();
					}
				}

				setState(2442);
				((CommandContext)_localctx).String = match(STRING);
				setState(2444);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2443);
					sed_op4();
					}
				}

				}
				break;
			case 18:
				enterOuterAlt(_localctx, 18);
				{
				setState(2446);
				match(T__15);
				setState(2448);
				_la = _input.LA(1);
				if (_la==T__91) {
					{
					setState(2447);
					sed_op0();
					}
				}

				setState(2451);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(2450);
					sed_op1();
					}
				}

				setState(2454);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(2453);
					sed_op2();
					}
				}

				setState(2457);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(2456);
					sed_op3();
					}
				}

				setState(2460);
				_la = _input.LA(1);
				if (_la==T__85) {
					{
					setState(2459);
					sed_op5();
					}
				}

				setState(2463);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2462);
					sed_op6();
					}
				}

				setState(2466);
				_la = _input.LA(1);
				if (_la==T__84) {
					{
					setState(2465);
					sed_op7();
					}
				}

				setState(2469);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2468);
					sed_op4();
					}
				}

				}
				break;
			case 19:
				enterOuterAlt(_localctx, 19);
				{
				setState(2471);
				match(T__16);
				setState(2473);
				_la = _input.LA(1);
				if (_la==T__52) {
					{
					setState(2472);
					awk_op0();
					}
				}

				setState(2476);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2475);
					awk_op1();
					}
				}

				setState(2479);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,505,_ctx) ) {
				case 1:
					{
					setState(2478);
					awk_op4();
					}
					break;
				}
				setState(2482);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2481);
					awk_op5();
					}
				}

				}
				break;
			case 20:
				enterOuterAlt(_localctx, 20);
				{
				setState(2484);
				match(T__17);
				setState(2486);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(2485);
					rm_op0();
					}
				}

				setState(2489);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2488);
					rm_op1();
					}
				}

				setState(2492);
				_la = _input.LA(1);
				if (_la==T__84) {
					{
					setState(2491);
					rm_op2();
					}
				}

				setState(2495);
				_la = _input.LA(1);
				if (_la==T__56) {
					{
					setState(2494);
					rm_op3();
					}
				}

				setState(2498);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(2497);
					rm_op4();
					}
				}

				setState(2501);
				_la = _input.LA(1);
				if (_la==T__10) {
					{
					setState(2500);
					rm_op5();
					}
				}

				setState(2504);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2503);
					rm_op6();
					}
				}

				setState(2507);
				_la = _input.LA(1);
				if (_la==T__111) {
					{
					setState(2506);
					rm_op7();
					}
				}

				setState(2510); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(2509);
					((CommandContext)_localctx).File = match(STRING);
					}
					}
					setState(2512); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==STRING );
				}
				break;
			case 21:
				enterOuterAlt(_localctx, 21);
				{
				setState(2514);
				match(T__18);
				setState(2516);
				_la = _input.LA(1);
				if (_la==T__56 || _la==T__83) {
					{
					setState(2515);
					cd_op0();
					}
				}

				setState(2519);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2518);
					cd_op1();
					}
				}

				}
				break;
			case 22:
				enterOuterAlt(_localctx, 22);
				{
				setState(2521);
				match(T__19);
				setState(2523);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(2522);
					wc_op0();
					}
				}

				setState(2526);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(2525);
					wc_op1();
					}
				}

				setState(2529);
				_la = _input.LA(1);
				if (_la==T__36) {
					{
					setState(2528);
					wc_op2();
					}
				}

				setState(2532);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(2531);
					wc_op3();
					}
				}

				setState(2535);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2534);
					wc_op4();
					}
				}

				}
				break;
			case 23:
				enterOuterAlt(_localctx, 23);
				{
				setState(2537);
				match(T__20);
				setState(2539);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2538);
					chmod_op0();
					}
				}

				setState(2542);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2541);
					chmod_op1();
					}
				}

				setState(2545);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(2544);
					chmod_op3();
					}
				}

				setState(2547);
				((CommandContext)_localctx).Permission = match(STRING);
				setState(2549); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(2548);
					((CommandContext)_localctx).File = match(STRING);
					}
					}
					setState(2551); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==STRING );
				}
				break;
			case 24:
				enterOuterAlt(_localctx, 24);
				{
				setState(2553);
				match(T__20);
				setState(2555);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2554);
					chmod_op0();
					}
				}

				setState(2558);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2557);
					chmod_op1();
					}
				}

				setState(2561);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(2560);
					chmod_op3();
					}
				}

				setState(2564);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,530,_ctx) ) {
				case 1:
					{
					setState(2563);
					chmod_op7();
					}
					break;
				}
				setState(2566);
				match(T__21);
				setState(2568); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(2567);
					((CommandContext)_localctx).File = match(STRING);
					}
					}
					setState(2570); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==STRING );
				}
				break;
			case 25:
				enterOuterAlt(_localctx, 25);
				{
				setState(2572);
				match(T__20);
				setState(2574);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2573);
					chmod_op0();
					}
				}

				setState(2577);
				_la = _input.LA(1);
				if (_la==T__94) {
					{
					setState(2576);
					chmod_op8();
					}
				}

				setState(2580);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2579);
					chmod_op1();
					}
				}

				setState(2583);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(2582);
					chmod_op3();
					}
				}

				setState(2586);
				_la = _input.LA(1);
				if (_la==T__91) {
					{
					setState(2585);
					chmod_op9();
					}
				}

				setState(2589); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(2588);
					((CommandContext)_localctx).File = match(STRING);
					}
					}
					setState(2591); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==STRING );
				}
				break;
			case 26:
				enterOuterAlt(_localctx, 26);
				{
				setState(2593);
				match(T__20);
				setState(2595);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2594);
					chmod_op0();
					}
				}

				setState(2598);
				_la = _input.LA(1);
				if (_la==T__94) {
					{
					setState(2597);
					chmod_op8();
					}
				}

				setState(2601);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2600);
					chmod_op1();
					}
				}

				setState(2604);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(2603);
					chmod_op3();
					}
				}

				setState(2607);
				_la = _input.LA(1);
				if (_la==T__60) {
					{
					setState(2606);
					chmod_op10();
					}
				}

				setState(2610); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(2609);
					((CommandContext)_localctx).File = match(STRING);
					}
					}
					setState(2612); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==STRING );
				}
				break;
			case 27:
				enterOuterAlt(_localctx, 27);
				{
				setState(2614);
				match(T__20);
				setState(2616);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2615);
					chmod_op0();
					}
				}

				setState(2619);
				_la = _input.LA(1);
				if (_la==T__94) {
					{
					setState(2618);
					chmod_op8();
					}
				}

				setState(2622);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2621);
					chmod_op1();
					}
				}

				setState(2625);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(2624);
					chmod_op3();
					}
				}

				setState(2628);
				_la = _input.LA(1);
				if (_la==T__105) {
					{
					setState(2627);
					chmod_op11();
					}
				}

				setState(2631); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(2630);
					((CommandContext)_localctx).File = match(STRING);
					}
					}
					setState(2633); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==STRING );
				}
				break;
			case 28:
				enterOuterAlt(_localctx, 28);
				{
				setState(2635);
				match(T__22);
				setState(2637);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2636);
					chown_op0();
					}
				}

				setState(2640);
				_la = _input.LA(1);
				if (_la==T__94) {
					{
					setState(2639);
					chown_op1();
					}
				}

				setState(2643);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2642);
					chown_op2();
					}
				}

				setState(2646);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(2645);
					chown_op4();
					}
				}

				setState(2648);
				((CommandContext)_localctx).String = match(STRING);
				setState(2650); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(2649);
					((CommandContext)_localctx).File = match(STRING);
					}
					}
					setState(2652); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==STRING );
				}
				break;
			case 29:
				enterOuterAlt(_localctx, 29);
				{
				setState(2654);
				match(T__23);
				setState(2656);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,555,_ctx) ) {
				case 1:
					{
					setState(2655);
					head_op2();
					}
					break;
				}
				setState(2659);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2658);
					head_op3();
					}
				}

				}
				break;
			case 30:
				enterOuterAlt(_localctx, 30);
				{
				setState(2661);
				match(T__24);
				setState(2663);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__1) | (1L << T__10) | (1L << T__52))) != 0)) {
					{
					setState(2662);
					tail_op0();
					}
				}

				setState(2666);
				_la = _input.LA(1);
				if (_la==T__62) {
					{
					setState(2665);
					tail_op1();
					}
				}

				setState(2669);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,559,_ctx) ) {
				case 1:
					{
					setState(2668);
					tail_op5();
					}
					break;
				}
				setState(2672);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2671);
					tail_op6();
					}
				}

				}
				break;
			case 31:
				enterOuterAlt(_localctx, 31);
				{
				setState(2674);
				match(T__25);
				setState(2676);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(2675);
					seq_op0();
					}
				}

				setState(2679);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2678);
					seq_op1();
					}
				}

				setState(2682);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(2681);
					seq_op2();
					}
				}

				setState(2685);
				_la = _input.LA(1);
				if (_la==T__12) {
					{
					setState(2684);
					seq_op3();
					}
				}

				setState(2688);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,565,_ctx) ) {
				case 1:
					{
					setState(2687);
					seq_op5();
					}
					break;
				}
				setState(2690);
				((CommandContext)_localctx).String = match(STRING);
				}
				break;
			case 32:
				enterOuterAlt(_localctx, 32);
				{
				setState(2691);
				match(T__26);
				setState(2692);
				((CommandContext)_localctx).File = match(STRING);
				}
				break;
			case 33:
				enterOuterAlt(_localctx, 33);
				{
				setState(2693);
				match(T__27);
				setState(2695);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(2694);
					cat_op0();
					}
				}

				setState(2698);
				_la = _input.LA(1);
				if (_la==T__85) {
					{
					setState(2697);
					cat_op1();
					}
				}

				setState(2701);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(2700);
					cat_op2();
					}
				}

				setState(2704);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(2703);
					cat_op3();
					}
				}

				setState(2707);
				_la = _input.LA(1);
				if (_la==T__12) {
					{
					setState(2706);
					cat_op4();
					}
				}

				setState(2710);
				_la = _input.LA(1);
				if (_la==T__11) {
					{
					setState(2709);
					cat_op5();
					}
				}

				setState(2713);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2712);
					cat_op6();
					}
				}

				setState(2716);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2715);
					cat_op7();
					}
				}

				}
				break;
			case 34:
				enterOuterAlt(_localctx, 34);
				{
				setState(2718);
				match(T__28);
				setState(2720);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(2719);
					zip_op0();
					}
				}

				setState(2723);
				_la = _input.LA(1);
				if (_la==T__63) {
					{
					setState(2722);
					zip_op1();
					}
				}

				setState(2726);
				_la = _input.LA(1);
				if (_la==T__120) {
					{
					setState(2725);
					zip_op2();
					}
				}

				setState(2729);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(2728);
					zip_op3();
					}
				}

				setState(2732);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(2731);
					zip_op4();
					}
				}

				setState(2735);
				_la = _input.LA(1);
				if (_la==T__139) {
					{
					setState(2734);
					zip_op5();
					}
				}

				setState(2738);
				_la = _input.LA(1);
				if (_la==T__85) {
					{
					setState(2737);
					zip_op6();
					}
				}

				setState(2741);
				_la = _input.LA(1);
				if (_la==T__91) {
					{
					setState(2740);
					zip_op7();
					}
				}

				setState(2744);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2743);
					zip_op8();
					}
				}

				setState(2747);
				_la = _input.LA(1);
				if (_la==T__52) {
					{
					setState(2746);
					zip_op9();
					}
				}

				setState(2750);
				_la = _input.LA(1);
				if (_la==T__37) {
					{
					setState(2749);
					zip_op10();
					}
				}

				setState(2753);
				_la = _input.LA(1);
				if (_la==T__94) {
					{
					setState(2752);
					zip_op11();
					}
				}

				setState(2756);
				_la = _input.LA(1);
				if (_la==T__53) {
					{
					setState(2755);
					zip_op12();
					}
				}

				setState(2759);
				_la = _input.LA(1);
				if (_la==T__64) {
					{
					setState(2758);
					zip_op13();
					}
				}

				setState(2762);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(2761);
					zip_op14();
					}
				}

				setState(2765);
				_la = _input.LA(1);
				if (_la==T__83) {
					{
					setState(2764);
					zip_op15();
					}
				}

				setState(2768);
				_la = _input.LA(1);
				if (_la==T__36) {
					{
					setState(2767);
					zip_op16();
					}
				}

				setState(2771);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(2770);
					zip_op17();
					}
				}

				setState(2774);
				_la = _input.LA(1);
				if (_la==T__62) {
					{
					setState(2773);
					zip_op18();
					}
				}

				setState(2777);
				_la = _input.LA(1);
				if (_la==T__10) {
					{
					setState(2776);
					zip_op19();
					}
				}

				setState(2780);
				_la = _input.LA(1);
				if (_la==T__89) {
					{
					setState(2779);
					zip_op20();
					}
				}

				setState(2783);
				_la = _input.LA(1);
				if (_la==T__55) {
					{
					setState(2782);
					zip_op21();
					}
				}

				setState(2786);
				_la = _input.LA(1);
				if (_la==T__47) {
					{
					setState(2785);
					zip_op22();
					}
				}

				setState(2789);
				_la = _input.LA(1);
				if (_la==T__11) {
					{
					setState(2788);
					zip_op23();
					}
				}

				setState(2792);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2791);
					zip_op24();
					}
				}

				setState(2795);
				_la = _input.LA(1);
				if (_la==T__115) {
					{
					setState(2794);
					zip_op25();
					}
				}

				setState(2798);
				_la = _input.LA(1);
				if (_la==T__41) {
					{
					setState(2797);
					zip_op26();
					}
				}

				setState(2801);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(2800);
					zip_op27();
					}
				}

				setState(2804);
				_la = _input.LA(1);
				if (_la==T__116) {
					{
					setState(2803);
					zip_op28();
					}
				}

				setState(2807);
				_la = _input.LA(1);
				if (_la==T__127) {
					{
					setState(2806);
					zip_op29();
					}
				}

				setState(2810);
				_la = _input.LA(1);
				if (_la==T__123) {
					{
					setState(2809);
					zip_op30();
					}
				}

				setState(2813);
				_la = _input.LA(1);
				if (_la==T__131) {
					{
					setState(2812);
					zip_op31();
					}
				}

				setState(2816);
				_la = _input.LA(1);
				if (_la==T__170) {
					{
					setState(2815);
					zip_op32();
					}
				}

				setState(2819);
				_la = _input.LA(1);
				if (_la==T__81) {
					{
					setState(2818);
					zip_op33();
					}
				}

				setState(2822);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(2821);
					zip_op34();
					}
				}

				setState(2825);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(2824);
					zip_op35();
					}
				}

				setState(2828);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,610,_ctx) ) {
				case 1:
					{
					setState(2827);
					zip_op36();
					}
					break;
				}
				setState(2831);
				_la = _input.LA(1);
				if (_la==T__12) {
					{
					setState(2830);
					zip_op37();
					}
				}

				setState(2834);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2833);
					zip_op39();
					}
				}

				setState(2837);
				_la = _input.LA(1);
				if (_la==T__168) {
					{
					setState(2836);
					zip_op40();
					}
				}

				}
				break;
			case 35:
				enterOuterAlt(_localctx, 35);
				{
				setState(2839);
				match(T__29);
				setState(2841);
				_la = _input.LA(1);
				if (_la==T__71) {
					{
					setState(2840);
					unzip_op0();
					}
				}

				setState(2844);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(2843);
					unzip_op1();
					}
				}

				setState(2847);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(2846);
					unzip_op2();
					}
				}

				setState(2850);
				_la = _input.LA(1);
				if (_la==T__78) {
					{
					setState(2849);
					unzip_op3();
					}
				}

				setState(2853);
				_la = _input.LA(1);
				if (_la==T__95) {
					{
					setState(2852);
					unzip_op4();
					}
				}

				setState(2856);
				_la = _input.LA(1);
				if (_la==T__12) {
					{
					setState(2855);
					unzip_op5();
					}
				}

				setState(2859);
				_la = _input.LA(1);
				if (_la==T__47) {
					{
					setState(2858);
					unzip_op6();
					}
				}

				setState(2862);
				_la = _input.LA(1);
				if (_la==T__11) {
					{
					setState(2861);
					unzip_op7();
					}
				}

				setState(2865);
				_la = _input.LA(1);
				if (_la==T__49) {
					{
					setState(2864);
					unzip_op8();
					}
				}

				setState(2868);
				_la = _input.LA(1);
				if (_la==T__127) {
					{
					setState(2867);
					unzip_op9();
					}
				}

				setState(2871);
				_la = _input.LA(1);
				if (_la==T__51) {
					{
					setState(2870);
					unzip_op10();
					}
				}

				setState(2874);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(2873);
					unzip_op11();
					}
				}

				setState(2877);
				_la = _input.LA(1);
				if (_la==T__53) {
					{
					setState(2876);
					unzip_op12();
					}
				}

				setState(2880);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(2879);
					unzip_op13();
					}
				}

				setState(2883);
				_la = _input.LA(1);
				if (_la==T__40) {
					{
					setState(2882);
					unzip_op14();
					}
				}

				setState(2886);
				_la = _input.LA(1);
				if (_la==T__62) {
					{
					setState(2885);
					unzip_op15();
					}
				}

				setState(2889);
				_la = _input.LA(1);
				if (_la==T__38) {
					{
					setState(2888);
					unzip_op16();
					}
				}

				setState(2892);
				_la = _input.LA(1);
				if (_la==T__60) {
					{
					setState(2891);
					unzip_op17();
					}
				}

				setState(2895);
				_la = _input.LA(1);
				if (_la==T__39) {
					{
					setState(2894);
					unzip_op18();
					}
				}

				setState(2898);
				_la = _input.LA(1);
				if (_la==T__83) {
					{
					setState(2897);
					unzip_op19();
					}
				}

				setState(2901);
				_la = _input.LA(1);
				if (_la==T__42) {
					{
					setState(2900);
					unzip_op20();
					}
				}

				setState(2904);
				_la = _input.LA(1);
				if (_la==T__115) {
					{
					setState(2903);
					unzip_op21();
					}
				}

				setState(2907);
				_la = _input.LA(1);
				if (_la==T__111) {
					{
					setState(2906);
					unzip_op22();
					}
				}

				setState(2910);
				_la = _input.LA(1);
				if (_la==T__74) {
					{
					setState(2909);
					unzip_op23();
					}
				}

				setState(2912);
				((CommandContext)_localctx).File = match(STRING);
				setState(2914);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2913);
					unzip_op24();
					}
				}

				setState(2917);
				_la = _input.LA(1);
				if (_la==T__13) {
					{
					setState(2916);
					unzip_op25();
					}
				}

				setState(2920);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(2919);
					unzip_op26();
					}
				}

				}
				break;
			case 36:
				enterOuterAlt(_localctx, 36);
				{
				setState(2922);
				match(T__30);
				setState(2924);
				_la = _input.LA(1);
				if (((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) {
					{
					setState(2923);
					du_op0();
					}
				}

				setState(2927);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,642,_ctx) ) {
				case 1:
					{
					setState(2926);
					du_op2();
					}
					break;
				}
				setState(2930);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(2929);
					du_op3();
					}
				}

				setState(2933);
				_la = _input.LA(1);
				if (((((_la - 37)) & ~0x3f) == 0 && ((1L << (_la - 37)) & ((1L << (T__36 - 37)) | (1L << (T__37 - 37)) | (1L << (T__64 - 37)) | (1L << (T__94 - 37)))) != 0)) {
					{
					setState(2932);
					du_op4();
					}
				}

				setState(2936);
				_la = _input.LA(1);
				if (_la==T__13) {
					{
					setState(2935);
					du_op5();
					}
				}

				setState(2939);
				_la = _input.LA(1);
				if (_la==T__103) {
					{
					setState(2938);
					du_op6();
					}
				}

				setState(2942);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2941);
					du_op7();
					}
				}

				}
				break;
			case 37:
				enterOuterAlt(_localctx, 37);
				{
				setState(2944);
				match(T__31);
				setState(2946);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(2945);
					echo_op0();
					}
				}

				setState(2949);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2948);
					echo_op1();
					}
				}

				}
				break;
			case 38:
				enterOuterAlt(_localctx, 38);
				{
				setState(2951);
				match(T__32);
				setState(2953);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,650,_ctx) ) {
				case 1:
					{
					setState(2952);
					diff_op0();
					}
					break;
				}
				setState(2956); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(2955);
					((CommandContext)_localctx).File = match(STRING);
					}
					}
					setState(2958); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==STRING );
				}
				break;
			case 39:
				enterOuterAlt(_localctx, 39);
				{
				setState(2960);
				match(T__33);
				setState(2962);
				_la = _input.LA(1);
				if (_la==T__153) {
					{
					setState(2961);
					comm_op0();
					}
				}

				setState(2965);
				_la = _input.LA(1);
				if (_la==T__114) {
					{
					setState(2964);
					comm_op1();
					}
				}

				setState(2968);
				_la = _input.LA(1);
				if (_la==T__50) {
					{
					setState(2967);
					comm_op2();
					}
				}

				setState(2971);
				_la = _input.LA(1);
				if (_la==T__84) {
					{
					setState(2970);
					comm_op3();
					}
				}

				setState(2973);
				((CommandContext)_localctx).File = match(STRING);
				setState(2974);
				((CommandContext)_localctx).File = match(STRING);
				}
				break;
			case 40:
				enterOuterAlt(_localctx, 40);
				{
				setState(2975);
				match(T__34);
				setState(2977);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,656,_ctx) ) {
				case 1:
					{
					setState(2976);
					sh_op0();
					}
					break;
				}
				setState(2980);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(2979);
					sh_op1();
					}
				}

				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op47Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op47Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op47; }
	}

	public final Tar_op47Context tar_op47() throws RecognitionException {
		Tar_op47Context _localctx = new Tar_op47Context(_ctx, getState());
		enterRule(_localctx, 2, RULE_tar_op47);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2984);
			match(T__35);
			setState(2985);
			((Tar_op47Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op2Context extends ParserRuleContext {
		public Unzip_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op2; }
	}

	public final Unzip_op2Context unzip_op2() throws RecognitionException {
		Unzip_op2Context _localctx = new Unzip_op2Context(_ctx, getState());
		enterRule(_localctx, 4, RULE_unzip_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2987);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op15Context extends ParserRuleContext {
		public Grep_op15Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op15; }
	}

	public final Grep_op15Context grep_op15() throws RecognitionException {
		Grep_op15Context _localctx = new Grep_op15Context(_ctx, getState());
		enterRule(_localctx, 6, RULE_grep_op15);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2989);
			match(T__36);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op21Context extends ParserRuleContext {
		public Ls_op21Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op21; }
	}

	public final Ls_op21Context ls_op21() throws RecognitionException {
		Ls_op21Context _localctx = new Ls_op21Context(_ctx, getState());
		enterRule(_localctx, 8, RULE_ls_op21);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2991);
			match(T__37);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cat_op3Context extends ParserRuleContext {
		public Cat_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cat_op3; }
	}

	public final Cat_op3Context cat_op3() throws RecognitionException {
		Cat_op3Context _localctx = new Cat_op3Context(_ctx, getState());
		enterRule(_localctx, 10, RULE_cat_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2993);
			match(T__38);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op2Context extends ParserRuleContext {
		public Sort_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op2; }
	}

	public final Sort_op2Context sort_op2() throws RecognitionException {
		Sort_op2Context _localctx = new Sort_op2Context(_ctx, getState());
		enterRule(_localctx, 12, RULE_sort_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2995);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op18Context extends ParserRuleContext {
		public Unzip_op18Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op18; }
	}

	public final Unzip_op18Context unzip_op18() throws RecognitionException {
		Unzip_op18Context _localctx = new Unzip_op18Context(_ctx, getState());
		enterRule(_localctx, 14, RULE_unzip_op18);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2997);
			match(T__39);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op28Context extends ParserRuleContext {
		public Ls_op28Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op28; }
	}

	public final Ls_op28Context ls_op28() throws RecognitionException {
		Ls_op28Context _localctx = new Ls_op28Context(_ctx, getState());
		enterRule(_localctx, 16, RULE_ls_op28);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(2999);
			match(T__40);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op26Context extends ParserRuleContext {
		public Zip_op26Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op26; }
	}

	public final Zip_op26Context zip_op26() throws RecognitionException {
		Zip_op26Context _localctx = new Zip_op26Context(_ctx, getState());
		enterRule(_localctx, 18, RULE_zip_op26);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3001);
			match(T__41);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op5Context extends ParserRuleContext {
		public Sort_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op5; }
	}

	public final Sort_op5Context sort_op5() throws RecognitionException {
		Sort_op5Context _localctx = new Sort_op5Context(_ctx, getState());
		enterRule(_localctx, 20, RULE_sort_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3003);
			match(T__42);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tail_op4Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tail_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tail_op4; }
	}

	public final Tail_op4Context tail_op4() throws RecognitionException {
		Tail_op4Context _localctx = new Tail_op4Context(_ctx, getState());
		enterRule(_localctx, 22, RULE_tail_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3005);
			match(T__43);
			setState(3006);
			((Tail_op4Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op15Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op15Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op15; }
	}

	public final Find_op15Context find_op15() throws RecognitionException {
		Find_op15Context _localctx = new Find_op15Context(_ctx, getState());
		enterRule(_localctx, 24, RULE_find_op15);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3008);
			match(T__44);
			setState(3009);
			((Find_op15Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op10Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Xargs_op9Context xargs_op9() {
			return getRuleContext(Xargs_op9Context.class,0);
		}
		public Xargs_op10Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op10; }
	}

	public final Xargs_op10Context xargs_op10() throws RecognitionException {
		Xargs_op10Context _localctx = new Xargs_op10Context(_ctx, getState());
		enterRule(_localctx, 26, RULE_xargs_op10);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3011);
			match(T__43);
			setState(3012);
			((Xargs_op10Context)_localctx).Number = match(STRING);
			setState(3014);
			_la = _input.LA(1);
			if (_la==T__13) {
				{
				setState(3013);
				xargs_op9();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op51Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op51Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op51; }
	}

	public final Find_op51Context find_op51() throws RecognitionException {
		Find_op51Context _localctx = new Find_op51Context(_ctx, getState());
		enterRule(_localctx, 28, RULE_find_op51);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3016);
			match(T__45);
			setState(3017);
			((Find_op51Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op16Context extends ParserRuleContext {
		public Zip_op16Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op16; }
	}

	public final Zip_op16Context zip_op16() throws RecognitionException {
		Zip_op16Context _localctx = new Zip_op16Context(_ctx, getState());
		enterRule(_localctx, 30, RULE_zip_op16);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3019);
			match(T__36);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op9Context extends ParserRuleContext {
		public Xargs_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op9; }
	}

	public final Xargs_op9Context xargs_op9() throws RecognitionException {
		Xargs_op9Context _localctx = new Xargs_op9Context(_ctx, getState());
		enterRule(_localctx, 32, RULE_xargs_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3021);
			match(T__13);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op38Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op38Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op38; }
	}

	public final Find_op38Context find_op38() throws RecognitionException {
		Find_op38Context _localctx = new Find_op38Context(_ctx, getState());
		enterRule(_localctx, 34, RULE_find_op38);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3023);
			match(T__46);
			setState(3024);
			((Find_op38Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op15Context extends ParserRuleContext {
		public Sort_op15Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op15; }
	}

	public final Sort_op15Context sort_op15() throws RecognitionException {
		Sort_op15Context _localctx = new Sort_op15Context(_ctx, getState());
		enterRule(_localctx, 36, RULE_sort_op15);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3026);
			match(T__47);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op12Context extends ParserRuleContext {
		public Ls_op12Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op12; }
	}

	public final Ls_op12Context ls_op12() throws RecognitionException {
		Ls_op12Context _localctx = new Ls_op12Context(_ctx, getState());
		enterRule(_localctx, 38, RULE_ls_op12);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3028);
			match(T__48);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op1Context extends ParserRuleContext {
		public Chmod_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op1; }
	}

	public final Chmod_op1Context chmod_op1() throws RecognitionException {
		Chmod_op1Context _localctx = new Chmod_op1Context(_ctx, getState());
		enterRule(_localctx, 40, RULE_chmod_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3030);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Comm_op2Context extends ParserRuleContext {
		public Comm_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comm_op2; }
	}

	public final Comm_op2Context comm_op2() throws RecognitionException {
		Comm_op2Context _localctx = new Comm_op2Context(_ctx, getState());
		enterRule(_localctx, 42, RULE_comm_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3032);
			match(T__50);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op0Context extends ParserRuleContext {
		public Egrep_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op0; }
	}

	public final Egrep_op0Context egrep_op0() throws RecognitionException {
		Egrep_op0Context _localctx = new Egrep_op0Context(_ctx, getState());
		enterRule(_localctx, 44, RULE_egrep_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3034);
			match(T__51);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Rm_op6Context extends ParserRuleContext {
		public Rm_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rm_op6; }
	}

	public final Rm_op6Context rm_op6() throws RecognitionException {
		Rm_op6Context _localctx = new Rm_op6Context(_ctx, getState());
		enterRule(_localctx, 46, RULE_rm_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3036);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op9Context extends ParserRuleContext {
		public Zip_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op9; }
	}

	public final Zip_op9Context zip_op9() throws RecognitionException {
		Zip_op9Context _localctx = new Zip_op9Context(_ctx, getState());
		enterRule(_localctx, 48, RULE_zip_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3038);
			match(T__52);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op12Context extends ParserRuleContext {
		public Zip_op12Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op12; }
	}

	public final Zip_op12Context zip_op12() throws RecognitionException {
		Zip_op12Context _localctx = new Zip_op12Context(_ctx, getState());
		enterRule(_localctx, 50, RULE_zip_op12);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3040);
			match(T__53);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op5Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Chmod_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op5; }
	}

	public final Chmod_op5Context chmod_op5() throws RecognitionException {
		Chmod_op5Context _localctx = new Chmod_op5Context(_ctx, getState());
		enterRule(_localctx, 52, RULE_chmod_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3042);
			match(T__54);
			setState(3043);
			((Chmod_op5Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op22Context extends ParserRuleContext {
		public Egrep_op22Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op22; }
	}

	public final Egrep_op22Context egrep_op22() throws RecognitionException {
		Egrep_op22Context _localctx = new Egrep_op22Context(_ctx, getState());
		enterRule(_localctx, 54, RULE_egrep_op22);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3045);
			match(T__55);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op34Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Egrep_op34Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op34; }
	}

	public final Egrep_op34Context egrep_op34() throws RecognitionException {
		Egrep_op34Context _localctx = new Egrep_op34Context(_ctx, getState());
		enterRule(_localctx, 56, RULE_egrep_op34);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3047);
			match(T__1);
			setState(3048);
			((Egrep_op34Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op24Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op24Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op24; }
	}

	public final Tar_op24Context tar_op24() throws RecognitionException {
		Tar_op24Context _localctx = new Tar_op24Context(_ctx, getState());
		enterRule(_localctx, 58, RULE_tar_op24);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3050);
			match(T__47);
			setState(3051);
			((Tar_op24Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Echo_op0Context extends ParserRuleContext {
		public Echo_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_echo_op0; }
	}

	public final Echo_op0Context echo_op0() throws RecognitionException {
		Echo_op0Context _localctx = new Echo_op0Context(_ctx, getState());
		enterRule(_localctx, 60, RULE_echo_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3053);
			match(T__43);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Rm_op3Context extends ParserRuleContext {
		public Rm_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rm_op3; }
	}

	public final Rm_op3Context rm_op3() throws RecognitionException {
		Rm_op3Context _localctx = new Rm_op3Context(_ctx, getState());
		enterRule(_localctx, 62, RULE_rm_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3055);
			match(T__56);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Du_op1Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Du_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_du_op1; }
	}

	public final Du_op1Context du_op1() throws RecognitionException {
		Du_op1Context _localctx = new Du_op1Context(_ctx, getState());
		enterRule(_localctx, 64, RULE_du_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3057);
			match(T__57);
			setState(3058);
			((Du_op1Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op69Context extends ParserRuleContext {
		public Find_op69Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op69; }
	}

	public final Find_op69Context find_op69() throws RecognitionException {
		Find_op69Context _localctx = new Find_op69Context(_ctx, getState());
		enterRule(_localctx, 66, RULE_find_op69);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3060);
			match(T__58);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op55Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op55Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op55; }
	}

	public final Find_op55Context find_op55() throws RecognitionException {
		Find_op55Context _localctx = new Find_op55Context(_ctx, getState());
		enterRule(_localctx, 68, RULE_find_op55);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3062);
			match(T__59);
			setState(3063);
			((Find_op55Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Rm_op0Context extends ParserRuleContext {
		public Rm_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rm_op0; }
	}

	public final Rm_op0Context rm_op0() throws RecognitionException {
		Rm_op0Context _localctx = new Rm_op0Context(_ctx, getState());
		enterRule(_localctx, 70, RULE_rm_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3065);
			match(T__57);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op2Context extends ParserRuleContext {
		public Ls_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op2; }
	}

	public final Ls_op2Context ls_op2() throws RecognitionException {
		Ls_op2Context _localctx = new Ls_op2Context(_ctx, getState());
		enterRule(_localctx, 72, RULE_ls_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3067);
			match(T__60);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op12Context extends ParserRuleContext {
		public Egrep_op12Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op12; }
	}

	public final Egrep_op12Context egrep_op12() throws RecognitionException {
		Egrep_op12Context _localctx = new Egrep_op12Context(_ctx, getState());
		enterRule(_localctx, 74, RULE_egrep_op12);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3069);
			match(T__61);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op38Context extends ParserRuleContext {
		public Tar_op38Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op38; }
	}

	public final Tar_op38Context tar_op38() throws RecognitionException {
		Tar_op38Context _localctx = new Tar_op38Context(_ctx, getState());
		enterRule(_localctx, 76, RULE_tar_op38);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3071);
			match(T__62);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op1Context extends ParserRuleContext {
		public Zip_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op1; }
	}

	public final Zip_op1Context zip_op1() throws RecognitionException {
		Zip_op1Context _localctx = new Zip_op1Context(_ctx, getState());
		enterRule(_localctx, 78, RULE_zip_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3073);
			match(T__63);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op86Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Find_op86Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op86; }
	}

	public final Find_op86Context find_op86() throws RecognitionException {
		Find_op86Context _localctx = new Find_op86Context(_ctx, getState());
		enterRule(_localctx, 80, RULE_find_op86);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3076); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3075);
				((Find_op86Context)_localctx).File = match(STRING);
				}
				}
				setState(3078); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op9Context extends ParserRuleContext {
		public Sort_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op9; }
	}

	public final Sort_op9Context sort_op9() throws RecognitionException {
		Sort_op9Context _localctx = new Sort_op9Context(_ctx, getState());
		enterRule(_localctx, 82, RULE_sort_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3080);
			match(T__64);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op45Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op45Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op45; }
	}

	public final Find_op45Context find_op45() throws RecognitionException {
		Find_op45Context _localctx = new Find_op45Context(_ctx, getState());
		enterRule(_localctx, 84, RULE_find_op45);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3082);
			match(T__65);
			setState(3083);
			((Find_op45Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Seq_op1Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Seq_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_seq_op1; }
	}

	public final Seq_op1Context seq_op1() throws RecognitionException {
		Seq_op1Context _localctx = new Seq_op1Context(_ctx, getState());
		enterRule(_localctx, 86, RULE_seq_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3085);
			match(T__1);
			setState(3086);
			((Seq_op1Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op37Context extends ParserRuleContext {
		public Token Time;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Zip_op37Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op37; }
	}

	public final Zip_op37Context zip_op37() throws RecognitionException {
		Zip_op37Context _localctx = new Zip_op37Context(_ctx, getState());
		enterRule(_localctx, 88, RULE_zip_op37);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3088);
			match(T__12);
			setState(3089);
			match(T__12);
			setState(3090);
			((Zip_op37Context)_localctx).Time = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op27Context extends ParserRuleContext {
		public Find_op27Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op27; }
	}

	public final Find_op27Context find_op27() throws RecognitionException {
		Find_op27Context _localctx = new Find_op27Context(_ctx, getState());
		enterRule(_localctx, 90, RULE_find_op27);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3092);
			match(T__66);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op82Context extends ParserRuleContext {
		public Find_op82Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op82; }
	}

	public final Find_op82Context find_op82() throws RecognitionException {
		Find_op82Context _localctx = new Find_op82Context(_ctx, getState());
		enterRule(_localctx, 92, RULE_find_op82);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3094);
			match(T__67);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op36Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op36Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op36; }
	}

	public final Find_op36Context find_op36() throws RecognitionException {
		Find_op36Context _localctx = new Find_op36Context(_ctx, getState());
		enterRule(_localctx, 94, RULE_find_op36);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3096);
			match(T__68);
			setState(3097);
			((Find_op36Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op7Context extends ParserRuleContext {
		public Find_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op7; }
	}

	public final Find_op7Context find_op7() throws RecognitionException {
		Find_op7Context _localctx = new Find_op7Context(_ctx, getState());
		enterRule(_localctx, 96, RULE_find_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3099);
			match(T__69);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op11Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Xargs_op11Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op11; }
	}

	public final Xargs_op11Context xargs_op11() throws RecognitionException {
		Xargs_op11Context _localctx = new Xargs_op11Context(_ctx, getState());
		enterRule(_localctx, 98, RULE_xargs_op11);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3101);
			match(T__56);
			setState(3102);
			((Xargs_op11Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op2Context extends ParserRuleContext {
		public Tar_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op2; }
	}

	public final Tar_op2Context tar_op2() throws RecognitionException {
		Tar_op2Context _localctx = new Tar_op2Context(_ctx, getState());
		enterRule(_localctx, 100, RULE_tar_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3104);
			match(T__70);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op29Context extends ParserRuleContext {
		public Grep_op29Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op29; }
	}

	public final Grep_op29Context grep_op29() throws RecognitionException {
		Grep_op29Context _localctx = new Grep_op29Context(_ctx, getState());
		enterRule(_localctx, 102, RULE_grep_op29);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3106);
			match(T__71);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Wc_op3Context extends ParserRuleContext {
		public Wc_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_wc_op3; }
	}

	public final Wc_op3Context wc_op3() throws RecognitionException {
		Wc_op3Context _localctx = new Wc_op3Context(_ctx, getState());
		enterRule(_localctx, 104, RULE_wc_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3108);
			match(T__41);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op63Context extends ParserRuleContext {
		public Token Utility;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op28Context find_op28() {
			return getRuleContext(Find_op28Context.class,0);
		}
		public Find_op63Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op63; }
	}

	public final Find_op63Context find_op63() throws RecognitionException {
		Find_op63Context _localctx = new Find_op63Context(_ctx, getState());
		enterRule(_localctx, 106, RULE_find_op63);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3110);
			match(T__72);
			setState(3111);
			((Find_op63Context)_localctx).Utility = match(STRING);
			setState(3113);
			_la = _input.LA(1);
			if (_la==STRING) {
				{
				setState(3112);
				find_op28();
				}
			}

			setState(3115);
			match(T__73);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op6Context extends ParserRuleContext {
		public Grep_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op6; }
	}

	public final Grep_op6Context grep_op6() throws RecognitionException {
		Grep_op6Context _localctx = new Grep_op6Context(_ctx, getState());
		enterRule(_localctx, 108, RULE_grep_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3117);
			match(T__52);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op5Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op5; }
	}

	public final Tar_op5Context tar_op5() throws RecognitionException {
		Tar_op5Context _localctx = new Tar_op5Context(_ctx, getState());
		enterRule(_localctx, 110, RULE_tar_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3119);
			match(T__1);
			setState(3120);
			((Tar_op5Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op12Context extends ParserRuleContext {
		public Token Size;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Xargs_op12Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op12; }
	}

	public final Xargs_op12Context xargs_op12() throws RecognitionException {
		Xargs_op12Context _localctx = new Xargs_op12Context(_ctx, getState());
		enterRule(_localctx, 112, RULE_xargs_op12);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3122);
			match(T__38);
			setState(3123);
			((Xargs_op12Context)_localctx).Size = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op33Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Tar_op33Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op33; }
	}

	public final Tar_op33Context tar_op33() throws RecognitionException {
		Tar_op33Context _localctx = new Tar_op33Context(_ctx, getState());
		enterRule(_localctx, 114, RULE_tar_op33);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3126); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3125);
				((Tar_op33Context)_localctx).File = match(STRING);
				}
				}
				setState(3128); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op2Context extends ParserRuleContext {
		public Find_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op2; }
	}

	public final Find_op2Context find_op2() throws RecognitionException {
		Find_op2Context _localctx = new Find_op2Context(_ctx, getState());
		enterRule(_localctx, 116, RULE_find_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3130);
			match(T__74);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op36Context extends ParserRuleContext {
		public Grep_op36Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op36; }
	}

	public final Grep_op36Context grep_op36() throws RecognitionException {
		Grep_op36Context _localctx = new Grep_op36Context(_ctx, getState());
		enterRule(_localctx, 118, RULE_grep_op36);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3132);
			match(T__75);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op19Context extends ParserRuleContext {
		public Zip_op19Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op19; }
	}

	public final Zip_op19Context zip_op19() throws RecognitionException {
		Zip_op19Context _localctx = new Zip_op19Context(_ctx, getState());
		enterRule(_localctx, 120, RULE_zip_op19);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3134);
			match(T__10);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op24Context extends ParserRuleContext {
		public Find_op24Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op24; }
	}

	public final Find_op24Context find_op24() throws RecognitionException {
		Find_op24Context _localctx = new Find_op24Context(_ctx, getState());
		enterRule(_localctx, 122, RULE_find_op24);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3136);
			match(T__76);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op21Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op21Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op21; }
	}

	public final Tar_op21Context tar_op21() throws RecognitionException {
		Tar_op21Context _localctx = new Tar_op21Context(_ctx, getState());
		enterRule(_localctx, 124, RULE_tar_op21);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3138);
			match(T__77);
			setState(3139);
			((Tar_op21Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sed_op2Context extends ParserRuleContext {
		public Sed_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sed_op2; }
	}

	public final Sed_op2Context sed_op2() throws RecognitionException {
		Sed_op2Context _localctx = new Sed_op2Context(_ctx, getState());
		enterRule(_localctx, 126, RULE_sed_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3141);
			match(T__78);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op71Context extends ParserRuleContext {
		public Find_op71Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op71; }
	}

	public final Find_op71Context find_op71() throws RecognitionException {
		Find_op71Context _localctx = new Find_op71Context(_ctx, getState());
		enterRule(_localctx, 128, RULE_find_op71);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3143);
			match(T__79);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op11Context extends ParserRuleContext {
		public Sort_op11Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op11; }
	}

	public final Sort_op11Context sort_op11() throws RecognitionException {
		Sort_op11Context _localctx = new Sort_op11Context(_ctx, getState());
		enterRule(_localctx, 130, RULE_sort_op11);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3145);
			match(T__40);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op25Context extends ParserRuleContext {
		public Find_op25Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op25; }
	}

	public final Find_op25Context find_op25() throws RecognitionException {
		Find_op25Context _localctx = new Find_op25Context(_ctx, getState());
		enterRule(_localctx, 132, RULE_find_op25);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3147);
			match(T__80);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op33Context extends ParserRuleContext {
		public Zip_op33Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op33; }
	}

	public final Zip_op33Context zip_op33() throws RecognitionException {
		Zip_op33Context _localctx = new Zip_op33Context(_ctx, getState());
		enterRule(_localctx, 134, RULE_zip_op33);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3149);
			match(T__81);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op35Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Zip_op35Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op35; }
	}

	public final Zip_op35Context zip_op35() throws RecognitionException {
		Zip_op35Context _localctx = new Zip_op35Context(_ctx, getState());
		enterRule(_localctx, 136, RULE_zip_op35);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3151);
			match(T__43);
			setState(3152);
			((Zip_op35Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op2Context extends ParserRuleContext {
		public Chmod_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op2; }
	}

	public final Chmod_op2Context chmod_op2() throws RecognitionException {
		Chmod_op2Context _localctx = new Chmod_op2Context(_ctx, getState());
		enterRule(_localctx, 138, RULE_chmod_op2);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3154);
			_la = _input.LA(1);
			if ( !(((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) ) {
			_errHandler.recoverInline(this);
			} else {
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cp_op3Context extends ParserRuleContext {
		public Cp_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cp_op3; }
	}

	public final Cp_op3Context cp_op3() throws RecognitionException {
		Cp_op3Context _localctx = new Cp_op3Context(_ctx, getState());
		enterRule(_localctx, 140, RULE_cp_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3156);
			match(T__84);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cat_op1Context extends ParserRuleContext {
		public Cat_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cat_op1; }
	}

	public final Cat_op1Context cat_op1() throws RecognitionException {
		Cat_op1Context _localctx = new Cat_op1Context(_ctx, getState());
		enterRule(_localctx, 142, RULE_cat_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3158);
			match(T__85);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sh_op1Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Sh_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sh_op1; }
	}

	public final Sh_op1Context sh_op1() throws RecognitionException {
		Sh_op1Context _localctx = new Sh_op1Context(_ctx, getState());
		enterRule(_localctx, 144, RULE_sh_op1);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3161); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3160);
				((Sh_op1Context)_localctx).File = match(STRING);
				}
				}
				setState(3163); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op0Context extends ParserRuleContext {
		public Find_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op0; }
	}

	public final Find_op0Context find_op0() throws RecognitionException {
		Find_op0Context _localctx = new Find_op0Context(_ctx, getState());
		enterRule(_localctx, 146, RULE_find_op0);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3165);
			_la = _input.LA(1);
			if ( !(((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) ) {
			_errHandler.recoverInline(this);
			} else {
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op34Context extends ParserRuleContext {
		public Ls_op34Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op34; }
	}

	public final Ls_op34Context ls_op34() throws RecognitionException {
		Ls_op34Context _localctx = new Ls_op34Context(_ctx, getState());
		enterRule(_localctx, 148, RULE_ls_op34);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3167);
			match(T__11);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op5Context extends ParserRuleContext {
		public Ls_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op5; }
	}

	public final Ls_op5Context ls_op5() throws RecognitionException {
		Ls_op5Context _localctx = new Ls_op5Context(_ctx, getState());
		enterRule(_localctx, 150, RULE_ls_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3169);
			match(T__82);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op7Context extends ParserRuleContext {
		public Egrep_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op7; }
	}

	public final Egrep_op7Context egrep_op7() throws RecognitionException {
		Egrep_op7Context _localctx = new Egrep_op7Context(_ctx, getState());
		enterRule(_localctx, 152, RULE_egrep_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3171);
			match(T__86);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op39Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Grep_op39Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op39; }
	}

	public final Grep_op39Context grep_op39() throws RecognitionException {
		Grep_op39Context _localctx = new Grep_op39Context(_ctx, getState());
		enterRule(_localctx, 154, RULE_grep_op39);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3173);
			((Grep_op39Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op35Context extends ParserRuleContext {
		public Token Number;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Egrep_op35Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op35; }
	}

	public final Egrep_op35Context egrep_op35() throws RecognitionException {
		Egrep_op35Context _localctx = new Egrep_op35Context(_ctx, getState());
		enterRule(_localctx, 156, RULE_egrep_op35);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(3175);
			match(T__87);
			setState(3179);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,664,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(3176);
					((Egrep_op35Context)_localctx).Number = match(STRING);
					}
					} 
				}
				setState(3181);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,664,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op32Context extends ParserRuleContext {
		public Token Utility;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op28Context find_op28() {
			return getRuleContext(Find_op28Context.class,0);
		}
		public Find_op32Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op32; }
	}

	public final Find_op32Context find_op32() throws RecognitionException {
		Find_op32Context _localctx = new Find_op32Context(_ctx, getState());
		enterRule(_localctx, 158, RULE_find_op32);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3182);
			match(T__88);
			setState(3183);
			((Find_op32Context)_localctx).Utility = match(STRING);
			setState(3185);
			_la = _input.LA(1);
			if (_la==STRING) {
				{
				setState(3184);
				find_op28();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op22Context extends ParserRuleContext {
		public Grep_op22Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op22; }
	}

	public final Grep_op22Context grep_op22() throws RecognitionException {
		Grep_op22Context _localctx = new Grep_op22Context(_ctx, getState());
		enterRule(_localctx, 160, RULE_grep_op22);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3187);
			match(T__55);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op3Context extends ParserRuleContext {
		public Chmod_op2Context chmod_op2() {
			return getRuleContext(Chmod_op2Context.class,0);
		}
		public Chmod_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op3; }
	}

	public final Chmod_op3Context chmod_op3() throws RecognitionException {
		Chmod_op3Context _localctx = new Chmod_op3Context(_ctx, getState());
		enterRule(_localctx, 162, RULE_chmod_op3);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3189);
			match(T__89);
			setState(3191);
			_la = _input.LA(1);
			if (((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) {
				{
				setState(3190);
				chmod_op2();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cat_op6Context extends ParserRuleContext {
		public Cat_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cat_op6; }
	}

	public final Cat_op6Context cat_op6() throws RecognitionException {
		Cat_op6Context _localctx = new Cat_op6Context(_ctx, getState());
		enterRule(_localctx, 164, RULE_cat_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3193);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op36Context extends ParserRuleContext {
		public Token Time;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Zip_op36Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op36; }
	}

	public final Zip_op36Context zip_op36() throws RecognitionException {
		Zip_op36Context _localctx = new Zip_op36Context(_ctx, getState());
		enterRule(_localctx, 166, RULE_zip_op36);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3195);
			match(T__12);
			setState(3196);
			((Zip_op36Context)_localctx).Time = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tail_op0Context extends ParserRuleContext {
		public Tail_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tail_op0; }
	}

	public final Tail_op0Context tail_op0() throws RecognitionException {
		Tail_op0Context _localctx = new Tail_op0Context(_ctx, getState());
		enterRule(_localctx, 168, RULE_tail_op0);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3198);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__1) | (1L << T__10) | (1L << T__52))) != 0)) ) {
			_errHandler.recoverInline(this);
			} else {
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sed_op6Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Sed_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sed_op6; }
	}

	public final Sed_op6Context sed_op6() throws RecognitionException {
		Sed_op6Context _localctx = new Sed_op6Context(_ctx, getState());
		enterRule(_localctx, 170, RULE_sed_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3200);
			match(T__1);
			setState(3201);
			((Sed_op6Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op44Context extends ParserRuleContext {
		public Tar_op44Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op44; }
	}

	public final Tar_op44Context tar_op44() throws RecognitionException {
		Tar_op44Context _localctx = new Tar_op44Context(_ctx, getState());
		enterRule(_localctx, 172, RULE_tar_op44);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3203);
			match(T__90);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sed_op0Context extends ParserRuleContext {
		public Sed_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sed_op0; }
	}

	public final Sed_op0Context sed_op0() throws RecognitionException {
		Sed_op0Context _localctx = new Sed_op0Context(_ctx, getState());
		enterRule(_localctx, 174, RULE_sed_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3205);
			match(T__91);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op46Context extends ParserRuleContext {
		public Tar_op46Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op46; }
	}

	public final Tar_op46Context tar_op46() throws RecognitionException {
		Tar_op46Context _localctx = new Tar_op46Context(_ctx, getState());
		enterRule(_localctx, 176, RULE_tar_op46);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3207);
			match(T__55);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op25Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Unzip_op25Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op25; }
	}

	public final Unzip_op25Context unzip_op25() throws RecognitionException {
		Unzip_op25Context _localctx = new Unzip_op25Context(_ctx, getState());
		enterRule(_localctx, 178, RULE_unzip_op25);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3209);
			match(T__13);
			setState(3211); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3210);
				((Unzip_op25Context)_localctx).File = match(STRING);
				}
				}
				setState(3213); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op66Context extends ParserRuleContext {
		public Token Permission;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op66Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op66; }
	}

	public final Find_op66Context find_op66() throws RecognitionException {
		Find_op66Context _localctx = new Find_op66Context(_ctx, getState());
		enterRule(_localctx, 180, RULE_find_op66);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3215);
			match(T__92);
			setState(3216);
			match(T__93);
			setState(3217);
			((Find_op66Context)_localctx).Permission = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op12Context extends ParserRuleContext {
		public Grep_op12Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op12; }
	}

	public final Grep_op12Context grep_op12() throws RecognitionException {
		Grep_op12Context _localctx = new Grep_op12Context(_ctx, getState());
		enterRule(_localctx, 182, RULE_grep_op12);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3219);
			match(T__61);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op29Context extends ParserRuleContext {
		public Egrep_op29Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op29; }
	}

	public final Egrep_op29Context egrep_op29() throws RecognitionException {
		Egrep_op29Context _localctx = new Egrep_op29Context(_ctx, getState());
		enterRule(_localctx, 184, RULE_egrep_op29);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3221);
			match(T__71);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op13Context extends ParserRuleContext {
		public Unzip_op13Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op13; }
	}

	public final Unzip_op13Context unzip_op13() throws RecognitionException {
		Unzip_op13Context _localctx = new Unzip_op13Context(_ctx, getState());
		enterRule(_localctx, 186, RULE_unzip_op13);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3223);
			match(T__43);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cp_op0Context extends ParserRuleContext {
		public Cp_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cp_op0; }
	}

	public final Cp_op0Context cp_op0() throws RecognitionException {
		Cp_op0Context _localctx = new Cp_op0Context(_ctx, getState());
		enterRule(_localctx, 188, RULE_cp_op0);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3225);
			_la = _input.LA(1);
			if ( !(((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) ) {
			_errHandler.recoverInline(this);
			} else {
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op7Context extends ParserRuleContext {
		public Tar_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op7; }
	}

	public final Tar_op7Context tar_op7() throws RecognitionException {
		Tar_op7Context _localctx = new Tar_op7Context(_ctx, getState());
		enterRule(_localctx, 190, RULE_tar_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3227);
			match(T__94);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op19Context extends ParserRuleContext {
		public Grep_op19Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op19; }
	}

	public final Grep_op19Context grep_op19() throws RecognitionException {
		Grep_op19Context _localctx = new Grep_op19Context(_ctx, getState());
		enterRule(_localctx, 192, RULE_grep_op19);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3229);
			match(T__95);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op12Context extends ParserRuleContext {
		public Token Time;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op12Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op12; }
	}

	public final Find_op12Context find_op12() throws RecognitionException {
		Find_op12Context _localctx = new Find_op12Context(_ctx, getState());
		enterRule(_localctx, 194, RULE_find_op12);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3231);
			match(T__96);
			setState(3232);
			((Find_op12Context)_localctx).Time = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op84Context extends ParserRuleContext {
		public Find_op84Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op84; }
	}

	public final Find_op84Context find_op84() throws RecognitionException {
		Find_op84Context _localctx = new Find_op84Context(_ctx, getState());
		enterRule(_localctx, 196, RULE_find_op84);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3234);
			match(T__97);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Awk_op0Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Awk_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_awk_op0; }
	}

	public final Awk_op0Context awk_op0() throws RecognitionException {
		Awk_op0Context _localctx = new Awk_op0Context(_ctx, getState());
		enterRule(_localctx, 198, RULE_awk_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3236);
			match(T__52);
			setState(3237);
			((Awk_op0Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op65Context extends ParserRuleContext {
		public Token Permission;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op65Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op65; }
	}

	public final Find_op65Context find_op65() throws RecognitionException {
		Find_op65Context _localctx = new Find_op65Context(_ctx, getState());
		enterRule(_localctx, 200, RULE_find_op65);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3239);
			match(T__92);
			setState(3240);
			((Find_op65Context)_localctx).Permission = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op13Context extends ParserRuleContext {
		public Find_op13Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op13; }
	}

	public final Find_op13Context find_op13() throws RecognitionException {
		Find_op13Context _localctx = new Find_op13Context(_ctx, getState());
		enterRule(_localctx, 202, RULE_find_op13);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3242);
			match(T__98);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op15Context extends ParserRuleContext {
		public Egrep_op15Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op15; }
	}

	public final Egrep_op15Context egrep_op15() throws RecognitionException {
		Egrep_op15Context _localctx = new Egrep_op15Context(_ctx, getState());
		enterRule(_localctx, 204, RULE_egrep_op15);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3244);
			match(T__36);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op42Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op42Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op42; }
	}

	public final Find_op42Context find_op42() throws RecognitionException {
		Find_op42Context _localctx = new Find_op42Context(_ctx, getState());
		enterRule(_localctx, 206, RULE_find_op42);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3246);
			match(T__99);
			setState(3247);
			((Find_op42Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op12Context extends ParserRuleContext {
		public Tar_op12Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op12; }
	}

	public final Tar_op12Context tar_op12() throws RecognitionException {
		Tar_op12Context _localctx = new Tar_op12Context(_ctx, getState());
		enterRule(_localctx, 208, RULE_tar_op12);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3249);
			match(T__78);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op2Context extends ParserRuleContext {
		public Grep_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op2; }
	}

	public final Grep_op2Context grep_op2() throws RecognitionException {
		Grep_op2Context _localctx = new Grep_op2Context(_ctx, getState());
		enterRule(_localctx, 210, RULE_grep_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3251);
			match(T__9);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op8Context extends ParserRuleContext {
		public Unzip_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op8; }
	}

	public final Unzip_op8Context unzip_op8() throws RecognitionException {
		Unzip_op8Context _localctx = new Unzip_op8Context(_ctx, getState());
		enterRule(_localctx, 212, RULE_unzip_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3253);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Du_op5Context extends ParserRuleContext {
		public Du_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_du_op5; }
	}

	public final Du_op5Context du_op5() throws RecognitionException {
		Du_op5Context _localctx = new Du_op5Context(_ctx, getState());
		enterRule(_localctx, 214, RULE_du_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3255);
			match(T__13);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op79Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op79Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op79; }
	}

	public final Find_op79Context find_op79() throws RecognitionException {
		Find_op79Context _localctx = new Find_op79Context(_ctx, getState());
		enterRule(_localctx, 216, RULE_find_op79);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3257);
			match(T__100);
			setState(3258);
			((Find_op79Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Awk_op3Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Awk_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_awk_op3; }
	}

	public final Awk_op3Context awk_op3() throws RecognitionException {
		Awk_op3Context _localctx = new Awk_op3Context(_ctx, getState());
		enterRule(_localctx, 218, RULE_awk_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3260);
			match(T__1);
			setState(3261);
			((Awk_op3Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op75Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op75Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op75; }
	}

	public final Find_op75Context find_op75() throws RecognitionException {
		Find_op75Context _localctx = new Find_op75Context(_ctx, getState());
		enterRule(_localctx, 220, RULE_find_op75);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3263);
			match(T__101);
			setState(3264);
			((Find_op75Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cp_op5Context extends ParserRuleContext {
		public Cp_op2Context cp_op2() {
			return getRuleContext(Cp_op2Context.class,0);
		}
		public Cp_op3Context cp_op3() {
			return getRuleContext(Cp_op3Context.class,0);
		}
		public Cp_op4Context cp_op4() {
			return getRuleContext(Cp_op4Context.class,0);
		}
		public Cp_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cp_op5; }
	}

	public final Cp_op5Context cp_op5() throws RecognitionException {
		Cp_op5Context _localctx = new Cp_op5Context(_ctx, getState());
		enterRule(_localctx, 222, RULE_cp_op5);
		int _la;
		try {
			setState(3275);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,671,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(3267);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(3266);
					cp_op2();
					}
				}

				setState(3270);
				_la = _input.LA(1);
				if (_la==T__84) {
					{
					setState(3269);
					cp_op3();
					}
				}

				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(3273);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(3272);
					cp_op4();
					}
				}

				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op18Context extends ParserRuleContext {
		public Ls_op18Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op18; }
	}

	public final Ls_op18Context ls_op18() throws RecognitionException {
		Ls_op18Context _localctx = new Ls_op18Context(_ctx, getState());
		enterRule(_localctx, 224, RULE_ls_op18);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3277);
			match(T__57);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Du_op3Context extends ParserRuleContext {
		public Du_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_du_op3; }
	}

	public final Du_op3Context du_op3() throws RecognitionException {
		Du_op3Context _localctx = new Du_op3Context(_ctx, getState());
		enterRule(_localctx, 226, RULE_du_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3279);
			match(T__9);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op25Context extends ParserRuleContext {
		public Ls_op25Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op25; }
	}

	public final Ls_op25Context ls_op25() throws RecognitionException {
		Ls_op25Context _localctx = new Ls_op25Context(_ctx, getState());
		enterRule(_localctx, 228, RULE_ls_op25);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3281);
			match(T__78);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Seq_op0Context extends ParserRuleContext {
		public Seq_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_seq_op0; }
	}

	public final Seq_op0Context seq_op0() throws RecognitionException {
		Seq_op0Context _localctx = new Seq_op0Context(_ctx, getState());
		enterRule(_localctx, 230, RULE_seq_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3283);
			match(T__41);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op74Context extends ParserRuleContext {
		public Token Size;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op74Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op74; }
	}

	public final Find_op74Context find_op74() throws RecognitionException {
		Find_op74Context _localctx = new Find_op74Context(_ctx, getState());
		enterRule(_localctx, 232, RULE_find_op74);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3285);
			match(T__102);
			setState(3286);
			((Find_op74Context)_localctx).Size = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op6Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op6; }
	}

	public final Find_op6Context find_op6() throws RecognitionException {
		Find_op6Context _localctx = new Find_op6Context(_ctx, getState());
		enterRule(_localctx, 234, RULE_find_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3288);
			match(T__1);
			setState(3289);
			((Find_op6Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op6Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Xargs_op5Context xargs_op5() {
			return getRuleContext(Xargs_op5Context.class,0);
		}
		public Xargs_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op6; }
	}

	public final Xargs_op6Context xargs_op6() throws RecognitionException {
		Xargs_op6Context _localctx = new Xargs_op6Context(_ctx, getState());
		enterRule(_localctx, 236, RULE_xargs_op6);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3291);
			match(T__103);
			setState(3292);
			((Xargs_op6Context)_localctx).String = match(STRING);
			setState(3294);
			_la = _input.LA(1);
			if (_la==T__89) {
				{
				setState(3293);
				xargs_op5();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op14Context extends ParserRuleContext {
		public Sort_op14Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op14; }
	}

	public final Sort_op14Context sort_op14() throws RecognitionException {
		Sort_op14Context _localctx = new Sort_op14Context(_ctx, getState());
		enterRule(_localctx, 238, RULE_sort_op14);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3296);
			match(T__12);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op11Context extends ParserRuleContext {
		public Ls_op11Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op11; }
	}

	public final Ls_op11Context ls_op11() throws RecognitionException {
		Ls_op11Context _localctx = new Ls_op11Context(_ctx, getState());
		enterRule(_localctx, 240, RULE_ls_op11);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3298);
			match(T__47);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op17Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op17Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op17; }
	}

	public final Tar_op17Context tar_op17() throws RecognitionException {
		Tar_op17Context _localctx = new Tar_op17Context(_ctx, getState());
		enterRule(_localctx, 242, RULE_tar_op17);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3300);
			match(T__104);
			setState(3301);
			((Tar_op17Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op28Context extends ParserRuleContext {
		public Grep_op28Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op28; }
	}

	public final Grep_op28Context grep_op28() throws RecognitionException {
		Grep_op28Context _localctx = new Grep_op28Context(_ctx, getState());
		enterRule(_localctx, 244, RULE_grep_op28);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3303);
			match(T__13);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tail_op5Context extends ParserRuleContext {
		public Tail_op2Context tail_op2() {
			return getRuleContext(Tail_op2Context.class,0);
		}
		public Tail_op3Context tail_op3() {
			return getRuleContext(Tail_op3Context.class,0);
		}
		public Tail_op4Context tail_op4() {
			return getRuleContext(Tail_op4Context.class,0);
		}
		public Tail_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tail_op5; }
	}

	public final Tail_op5Context tail_op5() throws RecognitionException {
		Tail_op5Context _localctx = new Tail_op5Context(_ctx, getState());
		enterRule(_localctx, 246, RULE_tail_op5);
		int _la;
		try {
			setState(3314);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,676,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(3306);
				_la = _input.LA(1);
				if (_la==T__107) {
					{
					setState(3305);
					tail_op2();
					}
				}

				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(3309);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(3308);
					tail_op3();
					}
				}

				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(3312);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(3311);
					tail_op4();
					}
				}

				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op43Context extends ParserRuleContext {
		public Tar_op43Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op43; }
	}

	public final Tar_op43Context tar_op43() throws RecognitionException {
		Tar_op43Context _localctx = new Tar_op43Context(_ctx, getState());
		enterRule(_localctx, 248, RULE_tar_op43);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3316);
			match(T__36);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op5Context extends ParserRuleContext {
		public Grep_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op5; }
	}

	public final Grep_op5Context grep_op5() throws RecognitionException {
		Grep_op5Context _localctx = new Grep_op5Context(_ctx, getState());
		enterRule(_localctx, 250, RULE_grep_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3318);
			match(T__91);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op11Context extends ParserRuleContext {
		public Egrep_op11Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op11; }
	}

	public final Egrep_op11Context egrep_op11() throws RecognitionException {
		Egrep_op11Context _localctx = new Egrep_op11Context(_ctx, getState());
		enterRule(_localctx, 252, RULE_egrep_op11);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3320);
			match(T__84);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op11Context extends ParserRuleContext {
		public Chmod_op11Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op11; }
	}

	public final Chmod_op11Context chmod_op11() throws RecognitionException {
		Chmod_op11Context _localctx = new Chmod_op11Context(_ctx, getState());
		enterRule(_localctx, 254, RULE_chmod_op11);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3322);
			match(T__105);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tail_op1Context extends ParserRuleContext {
		public Tail_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tail_op1; }
	}

	public final Tail_op1Context tail_op1() throws RecognitionException {
		Tail_op1Context _localctx = new Tail_op1Context(_ctx, getState());
		enterRule(_localctx, 256, RULE_tail_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3324);
			match(T__62);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op13Context extends ParserRuleContext {
		public Zip_op13Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op13; }
	}

	public final Zip_op13Context zip_op13() throws RecognitionException {
		Zip_op13Context _localctx = new Zip_op13Context(_ctx, getState());
		enterRule(_localctx, 258, RULE_zip_op13);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3326);
			match(T__64);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op57Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op57Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op57; }
	}

	public final Find_op57Context find_op57() throws RecognitionException {
		Find_op57Context _localctx = new Find_op57Context(_ctx, getState());
		enterRule(_localctx, 260, RULE_find_op57);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3328);
			match(T__106);
			setState(3329);
			((Find_op57Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op19Context extends ParserRuleContext {
		public Ls_op19Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op19; }
	}

	public final Ls_op19Context ls_op19() throws RecognitionException {
		Ls_op19Context _localctx = new Ls_op19Context(_ctx, getState());
		enterRule(_localctx, 262, RULE_ls_op19);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3331);
			match(T__85);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op22Context extends ParserRuleContext {
		public Tar_op22Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op22; }
	}

	public final Tar_op22Context tar_op22() throws RecognitionException {
		Tar_op22Context _localctx = new Tar_op22Context(_ctx, getState());
		enterRule(_localctx, 264, RULE_tar_op22);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3333);
			match(T__56);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op1Context extends ParserRuleContext {
		public Egrep_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op1; }
	}

	public final Egrep_op1Context egrep_op1() throws RecognitionException {
		Egrep_op1Context _localctx = new Egrep_op1Context(_ctx, getState());
		enterRule(_localctx, 266, RULE_egrep_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3335);
			match(T__107);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op72Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op72Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op72; }
	}

	public final Find_op72Context find_op72() throws RecognitionException {
		Find_op72Context _localctx = new Find_op72Context(_ctx, getState());
		enterRule(_localctx, 268, RULE_find_op72);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3337);
			match(T__108);
			setState(3338);
			((Find_op72Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op20Context extends ParserRuleContext {
		public Unzip_op20Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op20; }
	}

	public final Unzip_op20Context unzip_op20() throws RecognitionException {
		Unzip_op20Context _localctx = new Unzip_op20Context(_ctx, getState());
		enterRule(_localctx, 270, RULE_unzip_op20);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3340);
			match(T__42);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sed_op1Context extends ParserRuleContext {
		public Sed_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sed_op1; }
	}

	public final Sed_op1Context sed_op1() throws RecognitionException {
		Sed_op1Context _localctx = new Sed_op1Context(_ctx, getState());
		enterRule(_localctx, 272, RULE_sed_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3342);
			match(T__51);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op1Context extends ParserRuleContext {
		public Sort_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op1; }
	}

	public final Sort_op1Context sort_op1() throws RecognitionException {
		Sort_op1Context _localctx = new Sort_op1Context(_ctx, getState());
		enterRule(_localctx, 274, RULE_sort_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3344);
			match(T__57);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op41Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op41Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op41; }
	}

	public final Find_op41Context find_op41() throws RecognitionException {
		Find_op41Context _localctx = new Find_op41Context(_ctx, getState());
		enterRule(_localctx, 276, RULE_find_op41);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3346);
			match(T__109);
			setState(3347);
			((Find_op41Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op37Context extends ParserRuleContext {
		public Grep_op37Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op37; }
	}

	public final Grep_op37Context grep_op37() throws RecognitionException {
		Grep_op37Context _localctx = new Grep_op37Context(_ctx, getState());
		enterRule(_localctx, 278, RULE_grep_op37);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3349);
			match(T__110);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Rm_op7Context extends ParserRuleContext {
		public Rm_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rm_op7; }
	}

	public final Rm_op7Context rm_op7() throws RecognitionException {
		Rm_op7Context _localctx = new Rm_op7Context(_ctx, getState());
		enterRule(_localctx, 280, RULE_rm_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3351);
			match(T__111);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op6Context extends ParserRuleContext {
		public Zip_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op6; }
	}

	public final Zip_op6Context zip_op6() throws RecognitionException {
		Zip_op6Context _localctx = new Zip_op6Context(_ctx, getState());
		enterRule(_localctx, 282, RULE_zip_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3353);
			match(T__85);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op42Context extends ParserRuleContext {
		public Tar_op42Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op42; }
	}

	public final Tar_op42Context tar_op42() throws RecognitionException {
		Tar_op42Context _localctx = new Tar_op42Context(_ctx, getState());
		enterRule(_localctx, 284, RULE_tar_op42);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3355);
			match(T__112);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cat_op0Context extends ParserRuleContext {
		public Cat_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cat_op0; }
	}

	public final Cat_op0Context cat_op0() throws RecognitionException {
		Cat_op0Context _localctx = new Cat_op0Context(_ctx, getState());
		enterRule(_localctx, 286, RULE_cat_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3357);
			match(T__107);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cp_op8Context extends ParserRuleContext {
		public Cp_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cp_op8; }
	}

	public final Cp_op8Context cp_op8() throws RecognitionException {
		Cp_op8Context _localctx = new Cp_op8Context(_ctx, getState());
		enterRule(_localctx, 288, RULE_cp_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3359);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Wc_op1Context extends ParserRuleContext {
		public Wc_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_wc_op1; }
	}

	public final Wc_op1Context wc_op1() throws RecognitionException {
		Wc_op1Context _localctx = new Wc_op1Context(_ctx, getState());
		enterRule(_localctx, 290, RULE_wc_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3361);
			match(T__78);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op18Context extends ParserRuleContext {
		public Tar_op18Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op18; }
	}

	public final Tar_op18Context tar_op18() throws RecognitionException {
		Tar_op18Context _localctx = new Tar_op18Context(_ctx, getState());
		enterRule(_localctx, 292, RULE_tar_op18);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3363);
			match(T__113);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cp_op7Context extends ParserRuleContext {
		public Cp_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cp_op7; }
	}

	public final Cp_op7Context cp_op7() throws RecognitionException {
		Cp_op7Context _localctx = new Cp_op7Context(_ctx, getState());
		enterRule(_localctx, 294, RULE_cp_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3365);
			match(T__95);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op13Context extends ParserRuleContext {
		public Token Argument;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Xargs_op13Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op13; }
	}

	public final Xargs_op13Context xargs_op13() throws RecognitionException {
		Xargs_op13Context _localctx = new Xargs_op13Context(_ctx, getState());
		enterRule(_localctx, 296, RULE_xargs_op13);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3368); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3367);
				((Xargs_op13Context)_localctx).Argument = match(STRING);
				}
				}
				setState(3370); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op11Context extends ParserRuleContext {
		public Tar_op11Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op11; }
	}

	public final Tar_op11Context tar_op11() throws RecognitionException {
		Tar_op11Context _localctx = new Tar_op11Context(_ctx, getState());
		enterRule(_localctx, 298, RULE_tar_op11);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3372);
			match(T__83);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op0Context extends ParserRuleContext {
		public Chmod_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op0; }
	}

	public final Chmod_op0Context chmod_op0() throws RecognitionException {
		Chmod_op0Context _localctx = new Chmod_op0Context(_ctx, getState());
		enterRule(_localctx, 300, RULE_chmod_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3374);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Comm_op1Context extends ParserRuleContext {
		public Comm_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comm_op1; }
	}

	public final Comm_op1Context comm_op1() throws RecognitionException {
		Comm_op1Context _localctx = new Comm_op1Context(_ctx, getState());
		enterRule(_localctx, 302, RULE_comm_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3376);
			match(T__114);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op32Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Grep_op32Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op32; }
	}

	public final Grep_op32Context grep_op32() throws RecognitionException {
		Grep_op32Context _localctx = new Grep_op32Context(_ctx, getState());
		enterRule(_localctx, 304, RULE_grep_op32);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3378);
			match(T__60);
			setState(3379);
			((Grep_op32Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op25Context extends ParserRuleContext {
		public Egrep_op25Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op25; }
	}

	public final Egrep_op25Context egrep_op25() throws RecognitionException {
		Egrep_op25Context _localctx = new Egrep_op25Context(_ctx, getState());
		enterRule(_localctx, 306, RULE_egrep_op25);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3381);
			match(T__115);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op4Context extends ParserRuleContext {
		public Unzip_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op4; }
	}

	public final Unzip_op4Context unzip_op4() throws RecognitionException {
		Unzip_op4Context _localctx = new Unzip_op4Context(_ctx, getState());
		enterRule(_localctx, 308, RULE_unzip_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3383);
			match(T__95);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op30Context extends ParserRuleContext {
		public Tar_op30Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op30; }
	}

	public final Tar_op30Context tar_op30() throws RecognitionException {
		Tar_op30Context _localctx = new Tar_op30Context(_ctx, getState());
		enterRule(_localctx, 310, RULE_tar_op30);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3385);
			match(T__116);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op5Context extends ParserRuleContext {
		public Unzip_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op5; }
	}

	public final Unzip_op5Context unzip_op5() throws RecognitionException {
		Unzip_op5Context _localctx = new Unzip_op5Context(_ctx, getState());
		enterRule(_localctx, 312, RULE_unzip_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3387);
			match(T__12);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Seq_op3Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Seq_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_seq_op3; }
	}

	public final Seq_op3Context seq_op3() throws RecognitionException {
		Seq_op3Context _localctx = new Seq_op3Context(_ctx, getState());
		enterRule(_localctx, 314, RULE_seq_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3389);
			match(T__12);
			setState(3390);
			((Seq_op3Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op23Context extends ParserRuleContext {
		public Zip_op23Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op23; }
	}

	public final Zip_op23Context zip_op23() throws RecognitionException {
		Zip_op23Context _localctx = new Zip_op23Context(_ctx, getState());
		enterRule(_localctx, 316, RULE_zip_op23);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3392);
			match(T__11);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op17Context extends ParserRuleContext {
		public Zip_op17Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op17; }
	}

	public final Zip_op17Context zip_op17() throws RecognitionException {
		Zip_op17Context _localctx = new Zip_op17Context(_ctx, getState());
		enterRule(_localctx, 318, RULE_zip_op17);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3394);
			match(T__40);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op33Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op33Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op33; }
	}

	public final Find_op33Context find_op33() throws RecognitionException {
		Find_op33Context _localctx = new Find_op33Context(_ctx, getState());
		enterRule(_localctx, 320, RULE_find_op33);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3396);
			match(T__117);
			setState(3397);
			match(T__93);
			setState(3398);
			((Find_op33Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Comm_op3Context extends ParserRuleContext {
		public Comm_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comm_op3; }
	}

	public final Comm_op3Context comm_op3() throws RecognitionException {
		Comm_op3Context _localctx = new Comm_op3Context(_ctx, getState());
		enterRule(_localctx, 322, RULE_comm_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3400);
			match(T__84);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Du_op6Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Du_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_du_op6; }
	}

	public final Du_op6Context du_op6() throws RecognitionException {
		Du_op6Context _localctx = new Du_op6Context(_ctx, getState());
		enterRule(_localctx, 324, RULE_du_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3402);
			match(T__103);
			setState(3403);
			((Du_op6Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op14Context extends ParserRuleContext {
		public Grep_op14Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op14; }
	}

	public final Grep_op14Context grep_op14() throws RecognitionException {
		Grep_op14Context _localctx = new Grep_op14Context(_ctx, getState());
		enterRule(_localctx, 326, RULE_grep_op14);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3405);
			match(T__78);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op20Context extends ParserRuleContext {
		public Ls_op20Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op20; }
	}

	public final Ls_op20Context ls_op20() throws RecognitionException {
		Ls_op20Context _localctx = new Ls_op20Context(_ctx, getState());
		enterRule(_localctx, 328, RULE_ls_op20);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3407);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Wc_op4Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Wc_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_wc_op4; }
	}

	public final Wc_op4Context wc_op4() throws RecognitionException {
		Wc_op4Context _localctx = new Wc_op4Context(_ctx, getState());
		enterRule(_localctx, 330, RULE_wc_op4);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3410); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3409);
				((Wc_op4Context)_localctx).File = match(STRING);
				}
				}
				setState(3412); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op1Context extends ParserRuleContext {
		public Unzip_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op1; }
	}

	public final Unzip_op1Context unzip_op1() throws RecognitionException {
		Unzip_op1Context _localctx = new Unzip_op1Context(_ctx, getState());
		enterRule(_localctx, 332, RULE_unzip_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3414);
			match(T__9);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op56Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op56Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op56; }
	}

	public final Find_op56Context find_op56() throws RecognitionException {
		Find_op56Context _localctx = new Find_op56Context(_ctx, getState());
		enterRule(_localctx, 334, RULE_find_op56);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3416);
			match(T__118);
			setState(3417);
			((Find_op56Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op85Context extends ParserRuleContext {
		public Find_op85Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op85; }
	}

	public final Find_op85Context find_op85() throws RecognitionException {
		Find_op85Context _localctx = new Find_op85Context(_ctx, getState());
		enterRule(_localctx, 336, RULE_find_op85);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3419);
			match(T__119);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op7Context extends ParserRuleContext {
		public Chmod_op4Context chmod_op4() {
			return getRuleContext(Chmod_op4Context.class,0);
		}
		public Chmod_op5Context chmod_op5() {
			return getRuleContext(Chmod_op5Context.class,0);
		}
		public Chmod_op6Context chmod_op6() {
			return getRuleContext(Chmod_op6Context.class,0);
		}
		public Chmod_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op7; }
	}

	public final Chmod_op7Context chmod_op7() throws RecognitionException {
		Chmod_op7Context _localctx = new Chmod_op7Context(_ctx, getState());
		enterRule(_localctx, 338, RULE_chmod_op7);
		int _la;
		try {
			setState(3430);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,682,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(3422);
				_la = _input.LA(1);
				if (_la==T__93) {
					{
					setState(3421);
					chmod_op4();
					}
				}

				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(3425);
				_la = _input.LA(1);
				if (_la==T__54) {
					{
					setState(3424);
					chmod_op5();
					}
				}

				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(3428);
				_la = _input.LA(1);
				if (_la==T__146) {
					{
					setState(3427);
					chmod_op6();
					}
				}

				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op19Context extends ParserRuleContext {
		public Unzip_op19Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op19; }
	}

	public final Unzip_op19Context unzip_op19() throws RecognitionException {
		Unzip_op19Context _localctx = new Unzip_op19Context(_ctx, getState());
		enterRule(_localctx, 340, RULE_unzip_op19);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3432);
			match(T__83);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op8Context extends ParserRuleContext {
		public Ls_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op8; }
	}

	public final Ls_op8Context ls_op8() throws RecognitionException {
		Ls_op8Context _localctx = new Ls_op8Context(_ctx, getState());
		enterRule(_localctx, 342, RULE_ls_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3434);
			match(T__56);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op31Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Egrep_op31Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op31; }
	}

	public final Egrep_op31Context egrep_op31() throws RecognitionException {
		Egrep_op31Context _localctx = new Egrep_op31Context(_ctx, getState());
		enterRule(_localctx, 344, RULE_egrep_op31);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3436);
			match(T__120);
			setState(3437);
			((Egrep_op31Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op29Context extends ParserRuleContext {
		public Ls_op29Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op29; }
	}

	public final Ls_op29Context ls_op29() throws RecognitionException {
		Ls_op29Context _localctx = new Ls_op29Context(_ctx, getState());
		enterRule(_localctx, 346, RULE_ls_op29);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3439);
			match(T__95);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op48Context extends ParserRuleContext {
		public Tar_op48Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op48; }
	}

	public final Tar_op48Context tar_op48() throws RecognitionException {
		Tar_op48Context _localctx = new Tar_op48Context(_ctx, getState());
		enterRule(_localctx, 348, RULE_tar_op48);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3441);
			match(T__48);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op18Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Sort_op18Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op18; }
	}

	public final Sort_op18Context sort_op18() throws RecognitionException {
		Sort_op18Context _localctx = new Sort_op18Context(_ctx, getState());
		enterRule(_localctx, 350, RULE_sort_op18);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3444); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3443);
				((Sort_op18Context)_localctx).File = match(STRING);
				}
				}
				setState(3446); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op3Context extends ParserRuleContext {
		public Ls_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op3; }
	}

	public final Ls_op3Context ls_op3() throws RecognitionException {
		Ls_op3Context _localctx = new Ls_op3Context(_ctx, getState());
		enterRule(_localctx, 352, RULE_ls_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3448);
			match(T__52);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op30Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Grep_op30Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op30; }
	}

	public final Grep_op30Context grep_op30() throws RecognitionException {
		Grep_op30Context _localctx = new Grep_op30Context(_ctx, getState());
		enterRule(_localctx, 354, RULE_grep_op30);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3450);
			match(T__63);
			setState(3451);
			((Grep_op30Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op58Context extends ParserRuleContext {
		public Find_op58Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op58; }
	}

	public final Find_op58Context find_op58() throws RecognitionException {
		Find_op58Context _localctx = new Find_op58Context(_ctx, getState());
		enterRule(_localctx, 356, RULE_find_op58);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3453);
			match(T__121);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op1Context extends ParserRuleContext {
		public Grep_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op1; }
	}

	public final Grep_op1Context grep_op1() throws RecognitionException {
		Grep_op1Context _localctx = new Grep_op1Context(_ctx, getState());
		enterRule(_localctx, 358, RULE_grep_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3455);
			match(T__107);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op6Context extends ParserRuleContext {
		public Egrep_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op6; }
	}

	public final Egrep_op6Context egrep_op6() throws RecognitionException {
		Egrep_op6Context _localctx = new Egrep_op6Context(_ctx, getState());
		enterRule(_localctx, 360, RULE_egrep_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3457);
			match(T__52);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op37Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op37Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op37; }
	}

	public final Find_op37Context find_op37() throws RecognitionException {
		Find_op37Context _localctx = new Find_op37Context(_ctx, getState());
		enterRule(_localctx, 362, RULE_find_op37);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3459);
			match(T__122);
			setState(3460);
			((Find_op37Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op15Context extends ParserRuleContext {
		public Ls_op15Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op15; }
	}

	public final Ls_op15Context ls_op15() throws RecognitionException {
		Ls_op15Context _localctx = new Ls_op15Context(_ctx, getState());
		enterRule(_localctx, 364, RULE_ls_op15);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3462);
			match(T__51);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op26Context extends ParserRuleContext {
		public Tar_op26Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op26; }
	}

	public final Tar_op26Context tar_op26() throws RecognitionException {
		Tar_op26Context _localctx = new Tar_op26Context(_ctx, getState());
		enterRule(_localctx, 366, RULE_tar_op26);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3464);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cat_op7Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Cat_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cat_op7; }
	}

	public final Cat_op7Context cat_op7() throws RecognitionException {
		Cat_op7Context _localctx = new Cat_op7Context(_ctx, getState());
		enterRule(_localctx, 368, RULE_cat_op7);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3467); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3466);
				((Cat_op7Context)_localctx).File = match(STRING);
				}
				}
				setState(3469); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op14Context extends ParserRuleContext {
		public Ls_op14Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op14; }
	}

	public final Ls_op14Context ls_op14() throws RecognitionException {
		Ls_op14Context _localctx = new Ls_op14Context(_ctx, getState());
		enterRule(_localctx, 370, RULE_ls_op14);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3471);
			match(T__123);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op23Context extends ParserRuleContext {
		public Grep_op23Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op23; }
	}

	public final Grep_op23Context grep_op23() throws RecognitionException {
		Grep_op23Context _localctx = new Grep_op23Context(_ctx, getState());
		enterRule(_localctx, 372, RULE_grep_op23);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3473);
			match(T__38);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op8Context extends ParserRuleContext {
		public Tar_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op8; }
	}

	public final Tar_op8Context tar_op8() throws RecognitionException {
		Tar_op8Context _localctx = new Tar_op8Context(_ctx, getState());
		enterRule(_localctx, 374, RULE_tar_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3475);
			match(T__103);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op39Context extends ParserRuleContext {
		public Token Pattern;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Tar_op39Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op39; }
	}

	public final Tar_op39Context tar_op39() throws RecognitionException {
		Tar_op39Context _localctx = new Tar_op39Context(_ctx, getState());
		enterRule(_localctx, 376, RULE_tar_op39);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3478); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3477);
				((Tar_op39Context)_localctx).Pattern = match(STRING);
				}
				}
				setState(3480); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op39Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Egrep_op39Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op39; }
	}

	public final Egrep_op39Context egrep_op39() throws RecognitionException {
		Egrep_op39Context _localctx = new Egrep_op39Context(_ctx, getState());
		enterRule(_localctx, 378, RULE_egrep_op39);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3482);
			((Egrep_op39Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cp_op1Context extends ParserRuleContext {
		public Cp_op0Context cp_op0() {
			return getRuleContext(Cp_op0Context.class,0);
		}
		public Cp_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cp_op1; }
	}

	public final Cp_op1Context cp_op1() throws RecognitionException {
		Cp_op1Context _localctx = new Cp_op1Context(_ctx, getState());
		enterRule(_localctx, 380, RULE_cp_op1);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3484);
			match(T__89);
			setState(3486);
			_la = _input.LA(1);
			if (((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) {
				{
				setState(3485);
				cp_op0();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op16Context extends ParserRuleContext {
		public Token Time;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op16Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op16; }
	}

	public final Find_op16Context find_op16() throws RecognitionException {
		Find_op16Context _localctx = new Find_op16Context(_ctx, getState());
		enterRule(_localctx, 382, RULE_find_op16);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3488);
			match(T__51);
			setState(3489);
			match(T__12);
			setState(3490);
			match(T__84);
			setState(3491);
			match(T__36);
			setState(3492);
			match(T__85);
			setState(3493);
			((Find_op16Context)_localctx).Time = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op24Context extends ParserRuleContext {
		public Ls_op24Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op24; }
	}

	public final Ls_op24Context ls_op24() throws RecognitionException {
		Ls_op24Context _localctx = new Ls_op24Context(_ctx, getState());
		enterRule(_localctx, 384, RULE_ls_op24);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3495);
			match(T__64);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tail_op6Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Tail_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tail_op6; }
	}

	public final Tail_op6Context tail_op6() throws RecognitionException {
		Tail_op6Context _localctx = new Tail_op6Context(_ctx, getState());
		enterRule(_localctx, 386, RULE_tail_op6);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3498); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3497);
				((Tail_op6Context)_localctx).File = match(STRING);
				}
				}
				setState(3500); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op0Context extends ParserRuleContext {
		public Token Size;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op0; }
	}

	public final Tar_op0Context tar_op0() throws RecognitionException {
		Tar_op0Context _localctx = new Tar_op0Context(_ctx, getState());
		enterRule(_localctx, 388, RULE_tar_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3502);
			match(T__107);
			setState(3503);
			((Tar_op0Context)_localctx).Size = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op3Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op3; }
	}

	public final Tar_op3Context tar_op3() throws RecognitionException {
		Tar_op3Context _localctx = new Tar_op3Context(_ctx, getState());
		enterRule(_localctx, 390, RULE_tar_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3505);
			match(T__124);
			setState(3506);
			((Tar_op3Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op47Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op47Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op47; }
	}

	public final Find_op47Context find_op47() throws RecognitionException {
		Find_op47Context _localctx = new Find_op47Context(_ctx, getState());
		enterRule(_localctx, 392, RULE_find_op47);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3508);
			match(T__125);
			setState(3509);
			((Find_op47Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op9Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op9; }
	}

	public final Tar_op9Context tar_op9() throws RecognitionException {
		Tar_op9Context _localctx = new Tar_op9Context(_ctx, getState());
		enterRule(_localctx, 394, RULE_tar_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3511);
			match(T__126);
			setState(3512);
			((Tar_op9Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op26Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Unzip_op26Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op26; }
	}

	public final Unzip_op26Context unzip_op26() throws RecognitionException {
		Unzip_op26Context _localctx = new Unzip_op26Context(_ctx, getState());
		enterRule(_localctx, 396, RULE_unzip_op26);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3514);
			match(T__57);
			setState(3515);
			((Unzip_op26Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op9Context extends ParserRuleContext {
		public Unzip_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op9; }
	}

	public final Unzip_op9Context unzip_op9() throws RecognitionException {
		Unzip_op9Context _localctx = new Unzip_op9Context(_ctx, getState());
		enterRule(_localctx, 398, RULE_unzip_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3517);
			match(T__127);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op68Context extends ParserRuleContext {
		public Find_op68Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op68; }
	}

	public final Find_op68Context find_op68() throws RecognitionException {
		Find_op68Context _localctx = new Find_op68Context(_ctx, getState());
		enterRule(_localctx, 400, RULE_find_op68);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3519);
			match(T__128);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op38Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Zip_op38Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op38; }
	}

	public final Zip_op38Context zip_op38() throws RecognitionException {
		Zip_op38Context _localctx = new Zip_op38Context(_ctx, getState());
		enterRule(_localctx, 402, RULE_zip_op38);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3522); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3521);
				((Zip_op38Context)_localctx).File = match(STRING);
				}
				}
				setState(3524); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op44Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op44Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op44; }
	}

	public final Find_op44Context find_op44() throws RecognitionException {
		Find_op44Context _localctx = new Find_op44Context(_ctx, getState());
		enterRule(_localctx, 404, RULE_find_op44);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3526);
			match(T__129);
			setState(3527);
			((Find_op44Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op0Context extends ParserRuleContext {
		public Sort_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op0; }
	}

	public final Sort_op0Context sort_op0() throws RecognitionException {
		Sort_op0Context _localctx = new Sort_op0Context(_ctx, getState());
		enterRule(_localctx, 406, RULE_sort_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3529);
			match(T__107);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op52Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op52Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op52; }
	}

	public final Find_op52Context find_op52() throws RecognitionException {
		Find_op52Context _localctx = new Find_op52Context(_ctx, getState());
		enterRule(_localctx, 408, RULE_find_op52);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3531);
			match(T__130);
			setState(3532);
			((Find_op52Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op31Context extends ParserRuleContext {
		public Zip_op31Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op31; }
	}

	public final Zip_op31Context zip_op31() throws RecognitionException {
		Zip_op31Context _localctx = new Zip_op31Context(_ctx, getState());
		enterRule(_localctx, 410, RULE_zip_op31);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3534);
			match(T__131);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op49Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op49Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op49; }
	}

	public final Find_op49Context find_op49() throws RecognitionException {
		Find_op49Context _localctx = new Find_op49Context(_ctx, getState());
		enterRule(_localctx, 412, RULE_find_op49);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3536);
			match(T__132);
			setState(3537);
			((Find_op49Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op23Context extends ParserRuleContext {
		public Unzip_op23Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op23; }
	}

	public final Unzip_op23Context unzip_op23() throws RecognitionException {
		Unzip_op23Context _localctx = new Unzip_op23Context(_ctx, getState());
		enterRule(_localctx, 414, RULE_unzip_op23);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3539);
			match(T__74);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op16Context extends ParserRuleContext {
		public Egrep_op16Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op16; }
	}

	public final Egrep_op16Context egrep_op16() throws RecognitionException {
		Egrep_op16Context _localctx = new Egrep_op16Context(_ctx, getState());
		enterRule(_localctx, 416, RULE_egrep_op16);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3541);
			match(T__43);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op37Context extends ParserRuleContext {
		public Tar_op37Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op37; }
	}

	public final Tar_op37Context tar_op37() throws RecognitionException {
		Tar_op37Context _localctx = new Tar_op37Context(_ctx, getState());
		enterRule(_localctx, 418, RULE_tar_op37);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3543);
			match(T__133);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op10Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op10Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op10; }
	}

	public final Find_op10Context find_op10() throws RecognitionException {
		Find_op10Context _localctx = new Find_op10Context(_ctx, getState());
		enterRule(_localctx, 420, RULE_find_op10);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3545);
			match(T__134);
			setState(3546);
			((Find_op10Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op0Context extends ParserRuleContext {
		public Zip_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op0; }
	}

	public final Zip_op0Context zip_op0() throws RecognitionException {
		Zip_op0Context _localctx = new Zip_op0Context(_ctx, getState());
		enterRule(_localctx, 422, RULE_zip_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3548);
			match(T__51);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op33Context extends ParserRuleContext {
		public Ls_op33Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op33; }
	}

	public final Ls_op33Context ls_op33() throws RecognitionException {
		Ls_op33Context _localctx = new Ls_op33Context(_ctx, getState());
		enterRule(_localctx, 424, RULE_ls_op33);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3550);
			match(T__12);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op38Context extends ParserRuleContext {
		public Egrep_op38Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op38; }
	}

	public final Egrep_op38Context egrep_op38() throws RecognitionException {
		Egrep_op38Context _localctx = new Egrep_op38Context(_ctx, getState());
		enterRule(_localctx, 426, RULE_egrep_op38);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3552);
			match(T__135);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op10Context extends ParserRuleContext {
		public Sort_op10Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op10; }
	}

	public final Sort_op10Context sort_op10() throws RecognitionException {
		Sort_op10Context _localctx = new Sort_op10Context(_ctx, getState());
		enterRule(_localctx, 428, RULE_sort_op10);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3554);
			match(T__36);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op27Context extends ParserRuleContext {
		public Zip_op27Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op27; }
	}

	public final Zip_op27Context zip_op27() throws RecognitionException {
		Zip_op27Context _localctx = new Zip_op27Context(_ctx, getState());
		enterRule(_localctx, 430, RULE_zip_op27);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3556);
			match(T__74);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op11Context extends ParserRuleContext {
		public Unzip_op11Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op11; }
	}

	public final Unzip_op11Context unzip_op11() throws RecognitionException {
		Unzip_op11Context _localctx = new Unzip_op11Context(_ctx, getState());
		enterRule(_localctx, 432, RULE_unzip_op11);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3558);
			match(T__107);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op54Context extends ParserRuleContext {
		public Token Time;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op54Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op54; }
	}

	public final Find_op54Context find_op54() throws RecognitionException {
		Find_op54Context _localctx = new Find_op54Context(_ctx, getState());
		enterRule(_localctx, 434, RULE_find_op54);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3560);
			match(T__136);
			setState(3561);
			((Find_op54Context)_localctx).Time = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op5Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Xargs_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op5; }
	}

	public final Xargs_op5Context xargs_op5() throws RecognitionException {
		Xargs_op5Context _localctx = new Xargs_op5Context(_ctx, getState());
		enterRule(_localctx, 436, RULE_xargs_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3563);
			match(T__89);
			setState(3564);
			((Xargs_op5Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op21Context extends ParserRuleContext {
		public Egrep_op21Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op21; }
	}

	public final Egrep_op21Context egrep_op21() throws RecognitionException {
		Egrep_op21Context _localctx = new Egrep_op21Context(_ctx, getState());
		enterRule(_localctx, 438, RULE_egrep_op21);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3566);
			match(T__89);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op22Context extends ParserRuleContext {
		public Zip_op22Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op22; }
	}

	public final Zip_op22Context zip_op22() throws RecognitionException {
		Zip_op22Context _localctx = new Zip_op22Context(_ctx, getState());
		enterRule(_localctx, 440, RULE_zip_op22);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3568);
			match(T__47);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op8Context extends ParserRuleContext {
		public Find_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op8; }
	}

	public final Find_op8Context find_op8() throws RecognitionException {
		Find_op8Context _localctx = new Find_op8Context(_ctx, getState());
		enterRule(_localctx, 442, RULE_find_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3570);
			match(T__137);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op35Context extends ParserRuleContext {
		public Tar_op33Context tar_op33() {
			return getRuleContext(Tar_op33Context.class,0);
		}
		public Tar_op34Context tar_op34() {
			return getRuleContext(Tar_op34Context.class,0);
		}
		public Tar_op35Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op35; }
	}

	public final Tar_op35Context tar_op35() throws RecognitionException {
		Tar_op35Context _localctx = new Tar_op35Context(_ctx, getState());
		enterRule(_localctx, 444, RULE_tar_op35);
		int _la;
		try {
			setState(3578);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,691,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(3573);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(3572);
					tar_op33();
					}
				}

				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(3576);
				_la = _input.LA(1);
				if (_la==STRING) {
					{
					setState(3575);
					tar_op34();
					}
				}

				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op43Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op43Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op43; }
	}

	public final Find_op43Context find_op43() throws RecognitionException {
		Find_op43Context _localctx = new Find_op43Context(_ctx, getState());
		enterRule(_localctx, 446, RULE_find_op43);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3580);
			match(T__138);
			setState(3581);
			((Find_op43Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op14Context extends ParserRuleContext {
		public Unzip_op14Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op14; }
	}

	public final Unzip_op14Context unzip_op14() throws RecognitionException {
		Unzip_op14Context _localctx = new Unzip_op14Context(_ctx, getState());
		enterRule(_localctx, 448, RULE_unzip_op14);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3583);
			match(T__40);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op18Context extends ParserRuleContext {
		public Grep_op18Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op18; }
	}

	public final Grep_op18Context grep_op18() throws RecognitionException {
		Grep_op18Context _localctx = new Grep_op18Context(_ctx, getState());
		enterRule(_localctx, 450, RULE_grep_op18);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3585);
			match(T__40);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Head_op0Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Head_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_head_op0; }
	}

	public final Head_op0Context head_op0() throws RecognitionException {
		Head_op0Context _localctx = new Head_op0Context(_ctx, getState());
		enterRule(_localctx, 452, RULE_head_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3587);
			match(T__43);
			setState(3588);
			((Head_op0Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op26Context extends ParserRuleContext {
		public Egrep_op26Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op26; }
	}

	public final Egrep_op26Context egrep_op26() throws RecognitionException {
		Egrep_op26Context _localctx = new Egrep_op26Context(_ctx, getState());
		enterRule(_localctx, 454, RULE_egrep_op26);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3590);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op5Context extends ParserRuleContext {
		public Zip_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op5; }
	}

	public final Zip_op5Context zip_op5() throws RecognitionException {
		Zip_op5Context _localctx = new Zip_op5Context(_ctx, getState());
		enterRule(_localctx, 456, RULE_zip_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3592);
			match(T__139);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op2Context extends ParserRuleContext {
		public Xargs_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op2; }
	}

	public final Xargs_op2Context xargs_op2() throws RecognitionException {
		Xargs_op2Context _localctx = new Xargs_op2Context(_ctx, getState());
		enterRule(_localctx, 458, RULE_xargs_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3594);
			match(T__95);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op13Context extends ParserRuleContext {
		public Grep_op13Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op13; }
	}

	public final Grep_op13Context grep_op13() throws RecognitionException {
		Grep_op13Context _localctx = new Grep_op13Context(_ctx, getState());
		enterRule(_localctx, 460, RULE_grep_op13);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3596);
			match(T__83);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op17Context extends ParserRuleContext {
		public Unzip_op17Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op17; }
	}

	public final Unzip_op17Context unzip_op17() throws RecognitionException {
		Unzip_op17Context _localctx = new Unzip_op17Context(_ctx, getState());
		enterRule(_localctx, 462, RULE_unzip_op17);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3598);
			match(T__60);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op64Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op64Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op64; }
	}

	public final Find_op64Context find_op64() throws RecognitionException {
		Find_op64Context _localctx = new Find_op64Context(_ctx, getState());
		enterRule(_localctx, 464, RULE_find_op64);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3600);
			match(T__140);
			setState(3601);
			((Find_op64Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Mv_op1Context extends ParserRuleContext {
		public Mv_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mv_op1; }
	}

	public final Mv_op1Context mv_op1() throws RecognitionException {
		Mv_op1Context _localctx = new Mv_op1Context(_ctx, getState());
		enterRule(_localctx, 466, RULE_mv_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3603);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op50Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op50Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op50; }
	}

	public final Find_op50Context find_op50() throws RecognitionException {
		Find_op50Context _localctx = new Find_op50Context(_ctx, getState());
		enterRule(_localctx, 468, RULE_find_op50);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3605);
			match(T__141);
			setState(3606);
			((Find_op50Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op34Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Zip_op34Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op34; }
	}

	public final Zip_op34Context zip_op34() throws RecognitionException {
		Zip_op34Context _localctx = new Zip_op34Context(_ctx, getState());
		enterRule(_localctx, 470, RULE_zip_op34);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3608);
			match(T__107);
			setState(3609);
			((Zip_op34Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chown_op3Context extends ParserRuleContext {
		public Chown_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chown_op3; }
	}

	public final Chown_op3Context chown_op3() throws RecognitionException {
		Chown_op3Context _localctx = new Chown_op3Context(_ctx, getState());
		enterRule(_localctx, 472, RULE_chown_op3);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3611);
			_la = _input.LA(1);
			if ( !(((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) ) {
			_errHandler.recoverInline(this);
			} else {
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op40Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op40Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op40; }
	}

	public final Find_op40Context find_op40() throws RecognitionException {
		Find_op40Context _localctx = new Find_op40Context(_ctx, getState());
		enterRule(_localctx, 474, RULE_find_op40);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3613);
			match(T__142);
			setState(3614);
			((Find_op40Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op13Context extends ParserRuleContext {
		public Sort_op13Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op13; }
	}

	public final Sort_op13Context sort_op13() throws RecognitionException {
		Sort_op13Context _localctx = new Sort_op13Context(_ctx, getState());
		enterRule(_localctx, 476, RULE_sort_op13);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3616);
			match(T__55);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op7Context extends ParserRuleContext {
		public Zip_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op7; }
	}

	public final Zip_op7Context zip_op7() throws RecognitionException {
		Zip_op7Context _localctx = new Zip_op7Context(_ctx, getState());
		enterRule(_localctx, 478, RULE_zip_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3618);
			match(T__91);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op48Context extends ParserRuleContext {
		public Find_op48Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op48; }
	}

	public final Find_op48Context find_op48() throws RecognitionException {
		Find_op48Context _localctx = new Find_op48Context(_ctx, getState());
		enterRule(_localctx, 480, RULE_find_op48);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3620);
			match(T__143);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Wc_op2Context extends ParserRuleContext {
		public Wc_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_wc_op2; }
	}

	public final Wc_op2Context wc_op2() throws RecognitionException {
		Wc_op2Context _localctx = new Wc_op2Context(_ctx, getState());
		enterRule(_localctx, 482, RULE_wc_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3622);
			match(T__36);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op11Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op11Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op11; }
	}

	public final Find_op11Context find_op11() throws RecognitionException {
		Find_op11Context _localctx = new Find_op11Context(_ctx, getState());
		enterRule(_localctx, 484, RULE_find_op11);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3624);
			match(T__144);
			setState(3625);
			((Find_op11Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tail_op2Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tail_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tail_op2; }
	}

	public final Tail_op2Context tail_op2() throws RecognitionException {
		Tail_op2Context _localctx = new Tail_op2Context(_ctx, getState());
		enterRule(_localctx, 486, RULE_tail_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3627);
			match(T__107);
			setState(3628);
			((Tail_op2Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sed_op7Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Sed_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sed_op7; }
	}

	public final Sed_op7Context sed_op7() throws RecognitionException {
		Sed_op7Context _localctx = new Sed_op7Context(_ctx, getState());
		enterRule(_localctx, 488, RULE_sed_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3630);
			match(T__84);
			setState(3631);
			((Sed_op7Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op4Context extends ParserRuleContext {
		public Grep_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op4; }
	}

	public final Grep_op4Context grep_op4() throws RecognitionException {
		Grep_op4Context _localctx = new Grep_op4Context(_ctx, getState());
		enterRule(_localctx, 490, RULE_grep_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3633);
			match(T__139);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Seq_op5Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Seq_op4Context seq_op4() {
			return getRuleContext(Seq_op4Context.class,0);
		}
		public Seq_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_seq_op5; }
	}

	public final Seq_op5Context seq_op5() throws RecognitionException {
		Seq_op5Context _localctx = new Seq_op5Context(_ctx, getState());
		enterRule(_localctx, 492, RULE_seq_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3635);
			((Seq_op5Context)_localctx).String = match(STRING);
			setState(3637);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,692,_ctx) ) {
			case 1:
				{
				setState(3636);
				seq_op4();
				}
				break;
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op77Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op77Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op77; }
	}

	public final Find_op77Context find_op77() throws RecognitionException {
		Find_op77Context _localctx = new Find_op77Context(_ctx, getState());
		enterRule(_localctx, 494, RULE_find_op77);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3639);
			match(T__145);
			setState(3640);
			((Find_op77Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op30Context extends ParserRuleContext {
		public Zip_op30Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op30; }
	}

	public final Zip_op30Context zip_op30() throws RecognitionException {
		Zip_op30Context _localctx = new Zip_op30Context(_ctx, getState());
		enterRule(_localctx, 496, RULE_zip_op30);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3642);
			match(T__123);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op29Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op29Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op29; }
	}

	public final Tar_op29Context tar_op29() throws RecognitionException {
		Tar_op29Context _localctx = new Tar_op29Context(_ctx, getState());
		enterRule(_localctx, 498, RULE_tar_op29);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3644);
			match(T__74);
			setState(3645);
			((Tar_op29Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op6Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Chmod_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op6; }
	}

	public final Chmod_op6Context chmod_op6() throws RecognitionException {
		Chmod_op6Context _localctx = new Chmod_op6Context(_ctx, getState());
		enterRule(_localctx, 500, RULE_chmod_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3647);
			match(T__146);
			setState(3648);
			((Chmod_op6Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op9Context extends ParserRuleContext {
		public Chmod_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op9; }
	}

	public final Chmod_op9Context chmod_op9() throws RecognitionException {
		Chmod_op9Context _localctx = new Chmod_op9Context(_ctx, getState());
		enterRule(_localctx, 502, RULE_chmod_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3650);
			match(T__91);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op28Context extends ParserRuleContext {
		public Token Argument;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Find_op28Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op28; }
	}

	public final Find_op28Context find_op28() throws RecognitionException {
		Find_op28Context _localctx = new Find_op28Context(_ctx, getState());
		enterRule(_localctx, 504, RULE_find_op28);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3653); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3652);
				((Find_op28Context)_localctx).Argument = match(STRING);
				}
				}
				setState(3655); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cp_op4Context extends ParserRuleContext {
		public Cp_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cp_op4; }
	}

	public final Cp_op4Context cp_op4() throws RecognitionException {
		Cp_op4Context _localctx = new Cp_op4Context(_ctx, getState());
		enterRule(_localctx, 506, RULE_cp_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3657);
			match(T__43);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op10Context extends ParserRuleContext {
		public Egrep_op10Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op10; }
	}

	public final Egrep_op10Context egrep_op10() throws RecognitionException {
		Egrep_op10Context _localctx = new Egrep_op10Context(_ctx, getState());
		enterRule(_localctx, 508, RULE_egrep_op10);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3659);
			match(T__103);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op70Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op70Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op70; }
	}

	public final Find_op70Context find_op70() throws RecognitionException {
		Find_op70Context _localctx = new Find_op70Context(_ctx, getState());
		enterRule(_localctx, 510, RULE_find_op70);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3661);
			match(T__147);
			setState(3662);
			((Find_op70Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Head_op3Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Head_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_head_op3; }
	}

	public final Head_op3Context head_op3() throws RecognitionException {
		Head_op3Context _localctx = new Head_op3Context(_ctx, getState());
		enterRule(_localctx, 512, RULE_head_op3);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3665); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3664);
				((Head_op3Context)_localctx).File = match(STRING);
				}
				}
				setState(3667); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op0Context extends ParserRuleContext {
		public Xargs_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op0; }
	}

	public final Xargs_op0Context xargs_op0() throws RecognitionException {
		Xargs_op0Context _localctx = new Xargs_op0Context(_ctx, getState());
		enterRule(_localctx, 514, RULE_xargs_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3669);
			match(T__148);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Awk_op1Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Awk_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_awk_op1; }
	}

	public final Awk_op1Context awk_op1() throws RecognitionException {
		Awk_op1Context _localctx = new Awk_op1Context(_ctx, getState());
		enterRule(_localctx, 516, RULE_awk_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3671);
			match(T__49);
			setState(3672);
			((Awk_op1Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op36Context extends ParserRuleContext {
		public Ls_op36Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op36; }
	}

	public final Ls_op36Context ls_op36() throws RecognitionException {
		Ls_op36Context _localctx = new Ls_op36Context(_ctx, getState());
		enterRule(_localctx, 518, RULE_ls_op36);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3674);
			match(T__13);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op81Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op81Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op81; }
	}

	public final Find_op81Context find_op81() throws RecognitionException {
		Find_op81Context _localctx = new Find_op81Context(_ctx, getState());
		enterRule(_localctx, 520, RULE_find_op81);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3676);
			match(T__149);
			setState(3677);
			((Find_op81Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op20Context extends ParserRuleContext {
		public Grep_op20Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op20; }
	}

	public final Grep_op20Context grep_op20() throws RecognitionException {
		Grep_op20Context _localctx = new Grep_op20Context(_ctx, getState());
		enterRule(_localctx, 522, RULE_grep_op20);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3679);
			match(T__62);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tail_op3Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tail_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tail_op3; }
	}

	public final Tail_op3Context tail_op3() throws RecognitionException {
		Tail_op3Context _localctx = new Tail_op3Context(_ctx, getState());
		enterRule(_localctx, 524, RULE_tail_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3681);
			match(T__9);
			setState(3682);
			((Tail_op3Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op61Context extends ParserRuleContext {
		public Find_op61Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op61; }
	}

	public final Find_op61Context find_op61() throws RecognitionException {
		Find_op61Context _localctx = new Find_op61Context(_ctx, getState());
		enterRule(_localctx, 526, RULE_find_op61);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3684);
			match(T__150);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op40Context extends ParserRuleContext {
		public Tar_op40Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op40; }
	}

	public final Tar_op40Context tar_op40() throws RecognitionException {
		Tar_op40Context _localctx = new Tar_op40Context(_ctx, getState());
		enterRule(_localctx, 528, RULE_tar_op40);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3686);
			match(T__151);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op38Context extends ParserRuleContext {
		public Grep_op38Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op38; }
	}

	public final Grep_op38Context grep_op38() throws RecognitionException {
		Grep_op38Context _localctx = new Grep_op38Context(_ctx, getState());
		enterRule(_localctx, 530, RULE_grep_op38);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3688);
			match(T__135);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Rm_op2Context extends ParserRuleContext {
		public Rm_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rm_op2; }
	}

	public final Rm_op2Context rm_op2() throws RecognitionException {
		Rm_op2Context _localctx = new Rm_op2Context(_ctx, getState());
		enterRule(_localctx, 532, RULE_rm_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3690);
			match(T__84);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Mv_op0Context extends ParserRuleContext {
		public Mv_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mv_op0; }
	}

	public final Mv_op0Context mv_op0() throws RecognitionException {
		Mv_op0Context _localctx = new Mv_op0Context(_ctx, getState());
		enterRule(_localctx, 534, RULE_mv_op0);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3692);
			_la = _input.LA(1);
			if ( !(_la==T__1 || _la==T__43 || _la==T__84) ) {
			_errHandler.recoverInline(this);
			} else {
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op34Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Grep_op34Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op34; }
	}

	public final Grep_op34Context grep_op34() throws RecognitionException {
		Grep_op34Context _localctx = new Grep_op34Context(_ctx, getState());
		enterRule(_localctx, 536, RULE_grep_op34);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3694);
			match(T__1);
			setState(3695);
			((Grep_op34Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op20Context extends ParserRuleContext {
		public Tar_op20Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op20; }
	}

	public final Tar_op20Context tar_op20() throws RecognitionException {
		Tar_op20Context _localctx = new Tar_op20Context(_ctx, getState());
		enterRule(_localctx, 538, RULE_tar_op20);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3697);
			match(T__152);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op17Context extends ParserRuleContext {
		public Grep_op17Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op17; }
	}

	public final Grep_op17Context grep_op17() throws RecognitionException {
		Grep_op17Context _localctx = new Grep_op17Context(_ctx, getState());
		enterRule(_localctx, 540, RULE_grep_op17);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3699);
			match(T__133);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op31Context extends ParserRuleContext {
		public Token Utility;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op28Context find_op28() {
			return getRuleContext(Find_op28Context.class,0);
		}
		public Find_op31Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op31; }
	}

	public final Find_op31Context find_op31() throws RecognitionException {
		Find_op31Context _localctx = new Find_op31Context(_ctx, getState());
		enterRule(_localctx, 542, RULE_find_op31);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3701);
			match(T__88);
			setState(3702);
			((Find_op31Context)_localctx).Utility = match(STRING);
			setState(3704);
			_la = _input.LA(1);
			if (_la==STRING) {
				{
				setState(3703);
				find_op28();
				}
			}

			setState(3706);
			match(T__73);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op7Context extends ParserRuleContext {
		public Ls_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op7; }
	}

	public final Ls_op7Context ls_op7() throws RecognitionException {
		Ls_op7Context _localctx = new Ls_op7Context(_ctx, getState());
		enterRule(_localctx, 544, RULE_ls_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3708);
			match(T__133);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op37Context extends ParserRuleContext {
		public Ls_op37Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op37; }
	}

	public final Ls_op37Context ls_op37() throws RecognitionException {
		Ls_op37Context _localctx = new Ls_op37Context(_ctx, getState());
		enterRule(_localctx, 546, RULE_ls_op37);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3710);
			match(T__153);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op25Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op25Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op25; }
	}

	public final Tar_op25Context tar_op25() throws RecognitionException {
		Tar_op25Context _localctx = new Tar_op25Context(_ctx, getState());
		enterRule(_localctx, 548, RULE_tar_op25);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3712);
			match(T__154);
			setState(3713);
			((Tar_op25Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Awk_op4Context extends ParserRuleContext {
		public Awk_op2Context awk_op2() {
			return getRuleContext(Awk_op2Context.class,0);
		}
		public Awk_op3Context awk_op3() {
			return getRuleContext(Awk_op3Context.class,0);
		}
		public Awk_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_awk_op4; }
	}

	public final Awk_op4Context awk_op4() throws RecognitionException {
		Awk_op4Context _localctx = new Awk_op4Context(_ctx, getState());
		enterRule(_localctx, 550, RULE_awk_op4);
		int _la;
		try {
			setState(3721);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,698,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(3716);
				_errHandler.sync(this);
				switch ( getInterpreter().adaptivePredict(_input,696,_ctx) ) {
				case 1:
					{
					setState(3715);
					awk_op2();
					}
					break;
				}
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(3719);
				_la = _input.LA(1);
				if (_la==T__1) {
					{
					setState(3718);
					awk_op3();
					}
				}

				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op4Context extends ParserRuleContext {
		public Ls_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op4; }
	}

	public final Ls_op4Context ls_op4() throws RecognitionException {
		Ls_op4Context _localctx = new Ls_op4Context(_ctx, getState());
		enterRule(_localctx, 552, RULE_ls_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3723);
			match(T__86);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Comm_op0Context extends ParserRuleContext {
		public Comm_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_comm_op0; }
	}

	public final Comm_op0Context comm_op0() throws RecognitionException {
		Comm_op0Context _localctx = new Comm_op0Context(_ctx, getState());
		enterRule(_localctx, 554, RULE_comm_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3725);
			match(T__153);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op27Context extends ParserRuleContext {
		public Grep_op27Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op27; }
	}

	public final Grep_op27Context grep_op27() throws RecognitionException {
		Grep_op27Context _localctx = new Grep_op27Context(_ctx, getState());
		enterRule(_localctx, 556, RULE_grep_op27);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3727);
			match(T__41);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op35Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op35Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op35; }
	}

	public final Find_op35Context find_op35() throws RecognitionException {
		Find_op35Context _localctx = new Find_op35Context(_ctx, getState());
		enterRule(_localctx, 558, RULE_find_op35);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3729);
			match(T__117);
			setState(3730);
			((Find_op35Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op59Context extends ParserRuleContext {
		public Find_op59Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op59; }
	}

	public final Find_op59Context find_op59() throws RecognitionException {
		Find_op59Context _localctx = new Find_op59Context(_ctx, getState());
		enterRule(_localctx, 560, RULE_find_op59);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3732);
			match(T__155);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op24Context extends ParserRuleContext {
		public Egrep_op24Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op24; }
	}

	public final Egrep_op24Context egrep_op24() throws RecognitionException {
		Egrep_op24Context _localctx = new Egrep_op24Context(_ctx, getState());
		enterRule(_localctx, 562, RULE_egrep_op24);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3734);
			match(T__48);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op4Context extends ParserRuleContext {
		public Sort_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op4; }
	}

	public final Sort_op4Context sort_op4() throws RecognitionException {
		Sort_op4Context _localctx = new Sort_op4Context(_ctx, getState());
		enterRule(_localctx, 564, RULE_sort_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3736);
			match(T__84);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op31Context extends ParserRuleContext {
		public Tar_op31Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op31; }
	}

	public final Tar_op31Context tar_op31() throws RecognitionException {
		Tar_op31Context _localctx = new Tar_op31Context(_ctx, getState());
		enterRule(_localctx, 566, RULE_tar_op31);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3738);
			match(T__127);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op6Context extends ParserRuleContext {
		public Unzip_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op6; }
	}

	public final Unzip_op6Context unzip_op6() throws RecognitionException {
		Unzip_op6Context _localctx = new Unzip_op6Context(_ctx, getState());
		enterRule(_localctx, 568, RULE_unzip_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3740);
			match(T__47);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op33Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Grep_op33Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op33; }
	}

	public final Grep_op33Context grep_op33() throws RecognitionException {
		Grep_op33Context _localctx = new Grep_op33Context(_ctx, getState());
		enterRule(_localctx, 570, RULE_grep_op33);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3742);
			match(T__85);
			setState(3743);
			((Grep_op33Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op2Context extends ParserRuleContext {
		public Egrep_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op2; }
	}

	public final Egrep_op2Context egrep_op2() throws RecognitionException {
		Egrep_op2Context _localctx = new Egrep_op2Context(_ctx, getState());
		enterRule(_localctx, 572, RULE_egrep_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3745);
			match(T__9);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op24Context extends ParserRuleContext {
		public Zip_op24Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op24; }
	}

	public final Zip_op24Context zip_op24() throws RecognitionException {
		Zip_op24Context _localctx = new Zip_op24Context(_ctx, getState());
		enterRule(_localctx, 574, RULE_zip_op24);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3747);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cd_op1Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Cd_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cd_op1; }
	}

	public final Cd_op1Context cd_op1() throws RecognitionException {
		Cd_op1Context _localctx = new Cd_op1Context(_ctx, getState());
		enterRule(_localctx, 576, RULE_cd_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3749);
			((Cd_op1Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Rm_op4Context extends ParserRuleContext {
		public Rm_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rm_op4; }
	}

	public final Rm_op4Context rm_op4() throws RecognitionException {
		Rm_op4Context _localctx = new Rm_op4Context(_ctx, getState());
		enterRule(_localctx, 578, RULE_rm_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3751);
			match(T__89);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op14Context extends ParserRuleContext {
		public Token Time;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op14Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op14; }
	}

	public final Tar_op14Context tar_op14() throws RecognitionException {
		Tar_op14Context _localctx = new Tar_op14Context(_ctx, getState());
		enterRule(_localctx, 580, RULE_tar_op14);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3753);
			match(T__156);
			setState(3754);
			((Tar_op14Context)_localctx).Time = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Head_op2Context extends ParserRuleContext {
		public Head_op0Context head_op0() {
			return getRuleContext(Head_op0Context.class,0);
		}
		public Head_op1Context head_op1() {
			return getRuleContext(Head_op1Context.class,0);
		}
		public Head_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_head_op2; }
	}

	public final Head_op2Context head_op2() throws RecognitionException {
		Head_op2Context _localctx = new Head_op2Context(_ctx, getState());
		enterRule(_localctx, 582, RULE_head_op2);
		int _la;
		try {
			setState(3762);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,701,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(3757);
				_la = _input.LA(1);
				if (_la==T__43) {
					{
					setState(3756);
					head_op0();
					}
				}

				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(3760);
				_la = _input.LA(1);
				if (_la==T__9) {
					{
					setState(3759);
					head_op1();
					}
				}

				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Du_op2Context extends ParserRuleContext {
		public Du_op1Context du_op1() {
			return getRuleContext(Du_op1Context.class,0);
		}
		public Du_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_du_op2; }
	}

	public final Du_op2Context du_op2() throws RecognitionException {
		Du_op2Context _localctx = new Du_op2Context(_ctx, getState());
		enterRule(_localctx, 584, RULE_du_op2);
		int _la;
		try {
			setState(3769);
			switch (_input.LA(1)) {
			case T__51:
				enterOuterAlt(_localctx, 1);
				{
				setState(3764);
				match(T__51);
				}
				break;
			case T__38:
				enterOuterAlt(_localctx, 2);
				{
				setState(3765);
				match(T__38);
				}
				break;
			case EOF:
			case T__9:
			case T__13:
			case T__36:
			case T__37:
			case T__57:
			case T__64:
			case T__94:
			case T__103:
			case STRING:
				enterOuterAlt(_localctx, 3);
				{
				setState(3767);
				_la = _input.LA(1);
				if (_la==T__57) {
					{
					setState(3766);
					du_op1();
					}
				}

				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op0Context extends ParserRuleContext {
		public Ls_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op0; }
	}

	public final Ls_op0Context ls_op0() throws RecognitionException {
		Ls_op0Context _localctx = new Ls_op0Context(_ctx, getState());
		enterRule(_localctx, 586, RULE_ls_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3771);
			match(T__63);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op10Context extends ParserRuleContext {
		public Zip_op10Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op10; }
	}

	public final Zip_op10Context zip_op10() throws RecognitionException {
		Zip_op10Context _localctx = new Zip_op10Context(_ctx, getState());
		enterRule(_localctx, 588, RULE_zip_op10);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3773);
			match(T__37);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op7Context extends ParserRuleContext {
		public Sort_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op7; }
	}

	public final Sort_op7Context sort_op7() throws RecognitionException {
		Sort_op7Context _localctx = new Sort_op7Context(_ctx, getState());
		enterRule(_localctx, 590, RULE_sort_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3775);
			match(T__10);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sed_op5Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Sed_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sed_op5; }
	}

	public final Sed_op5Context sed_op5() throws RecognitionException {
		Sed_op5Context _localctx = new Sed_op5Context(_ctx, getState());
		enterRule(_localctx, 592, RULE_sed_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3777);
			match(T__85);
			setState(3778);
			((Sed_op5Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op18Context extends ParserRuleContext {
		public Egrep_op18Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op18; }
	}

	public final Egrep_op18Context egrep_op18() throws RecognitionException {
		Egrep_op18Context _localctx = new Egrep_op18Context(_ctx, getState());
		enterRule(_localctx, 594, RULE_egrep_op18);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3780);
			match(T__40);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op36Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op36Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op36; }
	}

	public final Tar_op36Context tar_op36() throws RecognitionException {
		Tar_op36Context _localctx = new Tar_op36Context(_ctx, getState());
		enterRule(_localctx, 596, RULE_tar_op36);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3782);
			match(T__157);
			setState(3783);
			((Tar_op36Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op13Context extends ParserRuleContext {
		public Egrep_op13Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op13; }
	}

	public final Egrep_op13Context egrep_op13() throws RecognitionException {
		Egrep_op13Context _localctx = new Egrep_op13Context(_ctx, getState());
		enterRule(_localctx, 598, RULE_egrep_op13);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3785);
			match(T__83);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op20Context extends ParserRuleContext {
		public Egrep_op20Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op20; }
	}

	public final Egrep_op20Context egrep_op20() throws RecognitionException {
		Egrep_op20Context _localctx = new Egrep_op20Context(_ctx, getState());
		enterRule(_localctx, 600, RULE_egrep_op20);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3787);
			match(T__62);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op18Context extends ParserRuleContext {
		public Zip_op18Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op18; }
	}

	public final Zip_op18Context zip_op18() throws RecognitionException {
		Zip_op18Context _localctx = new Zip_op18Context(_ctx, getState());
		enterRule(_localctx, 602, RULE_zip_op18);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3789);
			match(T__62);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op16Context extends ParserRuleContext {
		public Ls_op16Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op16; }
	}

	public final Ls_op16Context ls_op16() throws RecognitionException {
		Ls_op16Context _localctx = new Ls_op16Context(_ctx, getState());
		enterRule(_localctx, 604, RULE_ls_op16);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3791);
			match(T__107);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op10Context extends ParserRuleContext {
		public Tar_op10Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op10; }
	}

	public final Tar_op10Context tar_op10() throws RecognitionException {
		Tar_op10Context _localctx = new Tar_op10Context(_ctx, getState());
		enterRule(_localctx, 606, RULE_tar_op10);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3793);
			match(T__53);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op17Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op17Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op17; }
	}

	public final Find_op17Context find_op17() throws RecognitionException {
		Find_op17Context _localctx = new Find_op17Context(_ctx, getState());
		enterRule(_localctx, 608, RULE_find_op17);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3795);
			match(T__158);
			setState(3796);
			((Find_op17Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op0Context extends ParserRuleContext {
		public Grep_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op0; }
	}

	public final Grep_op0Context grep_op0() throws RecognitionException {
		Grep_op0Context _localctx = new Grep_op0Context(_ctx, getState());
		enterRule(_localctx, 610, RULE_grep_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3798);
			match(T__51);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op73Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op73Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op73; }
	}

	public final Find_op73Context find_op73() throws RecognitionException {
		Find_op73Context _localctx = new Find_op73Context(_ctx, getState());
		enterRule(_localctx, 612, RULE_find_op73);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3800);
			match(T__159);
			setState(3801);
			((Find_op73Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op53Context extends ParserRuleContext {
		public Find_op53Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op53; }
	}

	public final Find_op53Context find_op53() throws RecognitionException {
		Find_op53Context _localctx = new Find_op53Context(_ctx, getState());
		enterRule(_localctx, 614, RULE_find_op53);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3803);
			match(T__160);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op3Context extends ParserRuleContext {
		public Find_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op3; }
	}

	public final Find_op3Context find_op3() throws RecognitionException {
		Find_op3Context _localctx = new Find_op3Context(_ctx, getState());
		enterRule(_localctx, 616, RULE_find_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3805);
			match(T__57);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cp_op6Context extends ParserRuleContext {
		public Cp_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cp_op6; }
	}

	public final Cp_op6Context cp_op6() throws RecognitionException {
		Cp_op6Context _localctx = new Cp_op6Context(_ctx, getState());
		enterRule(_localctx, 618, RULE_cp_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3807);
			match(T__51);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op27Context extends ParserRuleContext {
		public Tar_op27Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op27; }
	}

	public final Tar_op27Context tar_op27() throws RecognitionException {
		Tar_op27Context _localctx = new Tar_op27Context(_ctx, getState());
		enterRule(_localctx, 620, RULE_tar_op27);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3809);
			match(T__161);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chown_op1Context extends ParserRuleContext {
		public Chown_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chown_op1; }
	}

	public final Chown_op1Context chown_op1() throws RecognitionException {
		Chown_op1Context _localctx = new Chown_op1Context(_ctx, getState());
		enterRule(_localctx, 622, RULE_chown_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3811);
			match(T__94);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Echo_op1Context extends ParserRuleContext {
		public Token String;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Echo_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_echo_op1; }
	}

	public final Echo_op1Context echo_op1() throws RecognitionException {
		Echo_op1Context _localctx = new Echo_op1Context(_ctx, getState());
		enterRule(_localctx, 624, RULE_echo_op1);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3814); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3813);
				((Echo_op1Context)_localctx).String = match(STRING);
				}
				}
				setState(3816); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op4Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op4; }
	}

	public final Tar_op4Context tar_op4() throws RecognitionException {
		Tar_op4Context _localctx = new Tar_op4Context(_ctx, getState());
		enterRule(_localctx, 626, RULE_tar_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3818);
			match(T__157);
			setState(3819);
			((Tar_op4Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op10Context extends ParserRuleContext {
		public Unzip_op10Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op10; }
	}

	public final Unzip_op10Context unzip_op10() throws RecognitionException {
		Unzip_op10Context _localctx = new Unzip_op10Context(_ctx, getState());
		enterRule(_localctx, 628, RULE_unzip_op10);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3821);
			match(T__51);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op1Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op1; }
	}

	public final Tar_op1Context tar_op1() throws RecognitionException {
		Tar_op1Context _localctx = new Tar_op1Context(_ctx, getState());
		enterRule(_localctx, 630, RULE_tar_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3823);
			match(T__60);
			setState(3824);
			((Tar_op1Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op3Context extends ParserRuleContext {
		public Xargs_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op3; }
	}

	public final Xargs_op3Context xargs_op3() throws RecognitionException {
		Xargs_op3Context _localctx = new Xargs_op3Context(_ctx, getState());
		enterRule(_localctx, 632, RULE_xargs_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3826);
			match(T__12);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Seq_op4Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Seq_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_seq_op4; }
	}

	public final Seq_op4Context seq_op4() throws RecognitionException {
		Seq_op4Context _localctx = new Seq_op4Context(_ctx, getState());
		enterRule(_localctx, 634, RULE_seq_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3828);
			((Seq_op4Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op8Context extends ParserRuleContext {
		public Chmod_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op8; }
	}

	public final Chmod_op8Context chmod_op8() throws RecognitionException {
		Chmod_op8Context _localctx = new Chmod_op8Context(_ctx, getState());
		enterRule(_localctx, 636, RULE_chmod_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3830);
			match(T__94);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op67Context extends ParserRuleContext {
		public Token Permission;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op67Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op67; }
	}

	public final Find_op67Context find_op67() throws RecognitionException {
		Find_op67Context _localctx = new Find_op67Context(_ctx, getState());
		enterRule(_localctx, 638, RULE_find_op67);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3832);
			match(T__92);
			setState(3833);
			match(T__54);
			setState(3834);
			((Find_op67Context)_localctx).Permission = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op17Context extends ParserRuleContext {
		public Egrep_op17Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op17; }
	}

	public final Egrep_op17Context egrep_op17() throws RecognitionException {
		Egrep_op17Context _localctx = new Egrep_op17Context(_ctx, getState());
		enterRule(_localctx, 640, RULE_egrep_op17);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3836);
			match(T__133);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cat_op2Context extends ParserRuleContext {
		public Cat_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cat_op2; }
	}

	public final Cat_op2Context cat_op2() throws RecognitionException {
		Cat_op2Context _localctx = new Cat_op2Context(_ctx, getState());
		enterRule(_localctx, 642, RULE_cat_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3838);
			match(T__43);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op17Context extends ParserRuleContext {
		public Sort_op17Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op17; }
	}

	public final Sort_op17Context sort_op17() throws RecognitionException {
		Sort_op17Context _localctx = new Sort_op17Context(_ctx, getState());
		enterRule(_localctx, 644, RULE_sort_op17);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3840);
			match(T__127);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op23Context extends ParserRuleContext {
		public Ls_op23Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op23; }
	}

	public final Ls_op23Context ls_op23() throws RecognitionException {
		Ls_op23Context _localctx = new Ls_op23Context(_ctx, getState());
		enterRule(_localctx, 646, RULE_ls_op23);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3842);
			match(T__84);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Wc_op0Context extends ParserRuleContext {
		public Wc_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_wc_op0; }
	}

	public final Wc_op0Context wc_op0() throws RecognitionException {
		Wc_op0Context _localctx = new Wc_op0Context(_ctx, getState());
		enterRule(_localctx, 648, RULE_wc_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3844);
			match(T__9);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op4Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Chmod_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op4; }
	}

	public final Chmod_op4Context chmod_op4() throws RecognitionException {
		Chmod_op4Context _localctx = new Chmod_op4Context(_ctx, getState());
		enterRule(_localctx, 650, RULE_chmod_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3846);
			match(T__93);
			setState(3847);
			((Chmod_op4Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op24Context extends ParserRuleContext {
		public Grep_op24Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op24; }
	}

	public final Grep_op24Context grep_op24() throws RecognitionException {
		Grep_op24Context _localctx = new Grep_op24Context(_ctx, getState());
		enterRule(_localctx, 652, RULE_grep_op24);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3849);
			match(T__48);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op28Context extends ParserRuleContext {
		public Zip_op28Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op28; }
	}

	public final Zip_op28Context zip_op28() throws RecognitionException {
		Zip_op28Context _localctx = new Zip_op28Context(_ctx, getState());
		enterRule(_localctx, 654, RULE_zip_op28);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3851);
			match(T__116);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op22Context extends ParserRuleContext {
		public Unzip_op22Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op22; }
	}

	public final Unzip_op22Context unzip_op22() throws RecognitionException {
		Unzip_op22Context _localctx = new Unzip_op22Context(_ctx, getState());
		enterRule(_localctx, 656, RULE_unzip_op22);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3853);
			match(T__111);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op34Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op34Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op34; }
	}

	public final Find_op34Context find_op34() throws RecognitionException {
		Find_op34Context _localctx = new Find_op34Context(_ctx, getState());
		enterRule(_localctx, 658, RULE_find_op34);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3855);
			match(T__117);
			setState(3856);
			match(T__54);
			setState(3857);
			((Find_op34Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op4Context extends ParserRuleContext {
		public Zip_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op4; }
	}

	public final Zip_op4Context zip_op4() throws RecognitionException {
		Zip_op4Context _localctx = new Zip_op4Context(_ctx, getState());
		enterRule(_localctx, 660, RULE_zip_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3859);
			match(T__57);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op27Context extends ParserRuleContext {
		public Egrep_op27Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op27; }
	}

	public final Egrep_op27Context egrep_op27() throws RecognitionException {
		Egrep_op27Context _localctx = new Egrep_op27Context(_ctx, getState());
		enterRule(_localctx, 662, RULE_egrep_op27);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3861);
			match(T__41);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op1Context extends ParserRuleContext {
		public Xargs_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op1; }
	}

	public final Xargs_op1Context xargs_op1() throws RecognitionException {
		Xargs_op1Context _localctx = new Xargs_op1Context(_ctx, getState());
		enterRule(_localctx, 664, RULE_xargs_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3863);
			match(T__40);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op32Context extends ParserRuleContext {
		public Ls_op32Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op32; }
	}

	public final Ls_op32Context ls_op32() throws RecognitionException {
		Ls_op32Context _localctx = new Ls_op32Context(_ctx, getState());
		enterRule(_localctx, 666, RULE_ls_op32);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3865);
			match(T__38);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op76Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op76Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op76; }
	}

	public final Find_op76Context find_op76() throws RecognitionException {
		Find_op76Context _localctx = new Find_op76Context(_ctx, getState());
		enterRule(_localctx, 668, RULE_find_op76);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3867);
			match(T__13);
			setState(3868);
			match(T__12);
			setState(3869);
			match(T__116);
			setState(3870);
			match(T__95);
			setState(3871);
			match(T__85);
			setState(3872);
			((Find_op76Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op40Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Grep_op40Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op40; }
	}

	public final Grep_op40Context grep_op40() throws RecognitionException {
		Grep_op40Context _localctx = new Grep_op40Context(_ctx, getState());
		enterRule(_localctx, 670, RULE_grep_op40);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3875); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3874);
				((Grep_op40Context)_localctx).File = match(STRING);
				}
				}
				setState(3877); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op5Context extends ParserRuleContext {
		public Egrep_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op5; }
	}

	public final Egrep_op5Context egrep_op5() throws RecognitionException {
		Egrep_op5Context _localctx = new Egrep_op5Context(_ctx, getState());
		enterRule(_localctx, 672, RULE_egrep_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3879);
			match(T__91);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op10Context extends ParserRuleContext {
		public Ls_op10Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op10; }
	}

	public final Ls_op10Context ls_op10() throws RecognitionException {
		Ls_op10Context _localctx = new Ls_op10Context(_ctx, getState());
		enterRule(_localctx, 674, RULE_ls_op10);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3881);
			match(T__55);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op15Context extends ParserRuleContext {
		public Unzip_op15Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op15; }
	}

	public final Unzip_op15Context unzip_op15() throws RecognitionException {
		Unzip_op15Context _localctx = new Unzip_op15Context(_ctx, getState());
		enterRule(_localctx, 676, RULE_unzip_op15);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3883);
			match(T__62);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op35Context extends ParserRuleContext {
		public Token Number;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Grep_op35Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op35; }
	}

	public final Grep_op35Context grep_op35() throws RecognitionException {
		Grep_op35Context _localctx = new Grep_op35Context(_ctx, getState());
		enterRule(_localctx, 678, RULE_grep_op35);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(3885);
			match(T__87);
			setState(3889);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,706,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(3886);
					((Grep_op35Context)_localctx).Number = match(STRING);
					}
					} 
				}
				setState(3891);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,706,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cat_op4Context extends ParserRuleContext {
		public Cat_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cat_op4; }
	}

	public final Cat_op4Context cat_op4() throws RecognitionException {
		Cat_op4Context _localctx = new Cat_op4Context(_ctx, getState());
		enterRule(_localctx, 680, RULE_cat_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3892);
			match(T__12);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op16Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op16Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op16; }
	}

	public final Tar_op16Context tar_op16() throws RecognitionException {
		Tar_op16Context _localctx = new Tar_op16Context(_ctx, getState());
		enterRule(_localctx, 682, RULE_tar_op16);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3894);
			match(T__162);
			setState(3895);
			((Tar_op16Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op14Context extends ParserRuleContext {
		public Zip_op14Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op14; }
	}

	public final Zip_op14Context zip_op14() throws RecognitionException {
		Zip_op14Context _localctx = new Zip_op14Context(_ctx, getState());
		enterRule(_localctx, 684, RULE_zip_op14);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3897);
			match(T__78);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op21Context extends ParserRuleContext {
		public Zip_op21Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op21; }
	}

	public final Zip_op21Context zip_op21() throws RecognitionException {
		Zip_op21Context _localctx = new Zip_op21Context(_ctx, getState());
		enterRule(_localctx, 686, RULE_zip_op21);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3899);
			match(T__55);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op24Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Unzip_op24Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op24; }
	}

	public final Unzip_op24Context unzip_op24() throws RecognitionException {
		Unzip_op24Context _localctx = new Unzip_op24Context(_ctx, getState());
		enterRule(_localctx, 688, RULE_unzip_op24);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3902); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3901);
				((Unzip_op24Context)_localctx).File = match(STRING);
				}
				}
				setState(3904); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op9Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op9; }
	}

	public final Find_op9Context find_op9() throws RecognitionException {
		Find_op9Context _localctx = new Find_op9Context(_ctx, getState());
		enterRule(_localctx, 690, RULE_find_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3906);
			match(T__97);
			setState(3907);
			((Find_op9Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op60Context extends ParserRuleContext {
		public Find_op60Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op60; }
	}

	public final Find_op60Context find_op60() throws RecognitionException {
		Find_op60Context _localctx = new Find_op60Context(_ctx, getState());
		enterRule(_localctx, 692, RULE_find_op60);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3909);
			match(T__163);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op8Context extends ParserRuleContext {
		public Zip_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op8; }
	}

	public final Zip_op8Context zip_op8() throws RecognitionException {
		Zip_op8Context _localctx = new Zip_op8Context(_ctx, getState());
		enterRule(_localctx, 694, RULE_zip_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3911);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Rm_op1Context extends ParserRuleContext {
		public Rm_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rm_op1; }
	}

	public final Rm_op1Context rm_op1() throws RecognitionException {
		Rm_op1Context _localctx = new Rm_op1Context(_ctx, getState());
		enterRule(_localctx, 696, RULE_rm_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3913);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op19Context extends ParserRuleContext {
		public Tar_op19Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op19; }
	}

	public final Tar_op19Context tar_op19() throws RecognitionException {
		Tar_op19Context _localctx = new Tar_op19Context(_ctx, getState());
		enterRule(_localctx, 698, RULE_tar_op19);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3915);
			match(T__40);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op30Context extends ParserRuleContext {
		public Ls_op30Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op30; }
	}

	public final Ls_op30Context ls_op30() throws RecognitionException {
		Ls_op30Context _localctx = new Ls_op30Context(_ctx, getState());
		enterRule(_localctx, 700, RULE_ls_op30);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3917);
			match(T__62);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op6Context extends ParserRuleContext {
		public Sort_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op6; }
	}

	public final Sort_op6Context sort_op6() throws RecognitionException {
		Sort_op6Context _localctx = new Sort_op6Context(_ctx, getState());
		enterRule(_localctx, 702, RULE_sort_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3919);
			match(T__43);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op25Context extends ParserRuleContext {
		public Zip_op25Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op25; }
	}

	public final Zip_op25Context zip_op25() throws RecognitionException {
		Zip_op25Context _localctx = new Zip_op25Context(_ctx, getState());
		enterRule(_localctx, 704, RULE_zip_op25);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3921);
			match(T__115);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op22Context extends ParserRuleContext {
		public Ls_op22Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op22; }
	}

	public final Ls_op22Context ls_op22() throws RecognitionException {
		Ls_op22Context _localctx = new Ls_op22Context(_ctx, getState());
		enterRule(_localctx, 706, RULE_ls_op22);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3923);
			match(T__94);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op83Context extends ParserRuleContext {
		public Find_op83Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op83; }
	}

	public final Find_op83Context find_op83() throws RecognitionException {
		Find_op83Context _localctx = new Find_op83Context(_ctx, getState());
		enterRule(_localctx, 708, RULE_find_op83);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3925);
			match(T__164);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op32Context extends ParserRuleContext {
		public Tar_op32Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op32; }
	}

	public final Tar_op32Context tar_op32() throws RecognitionException {
		Tar_op32Context _localctx = new Tar_op32Context(_ctx, getState());
		enterRule(_localctx, 710, RULE_tar_op32);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3927);
			match(T__71);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op16Context extends ParserRuleContext {
		public Grep_op16Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op16; }
	}

	public final Grep_op16Context grep_op16() throws RecognitionException {
		Grep_op16Context _localctx = new Grep_op16Context(_ctx, getState());
		enterRule(_localctx, 712, RULE_grep_op16);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3929);
			match(T__43);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op39Context extends ParserRuleContext {
		public Find_op39Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op39; }
	}

	public final Find_op39Context find_op39() throws RecognitionException {
		Find_op39Context _localctx = new Find_op39Context(_ctx, getState());
		enterRule(_localctx, 714, RULE_find_op39);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3931);
			match(T__165);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op9Context extends ParserRuleContext {
		public Grep_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op9; }
	}

	public final Grep_op9Context grep_op9() throws RecognitionException {
		Grep_op9Context _localctx = new Grep_op9Context(_ctx, getState());
		enterRule(_localctx, 716, RULE_grep_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3933);
			match(T__94);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op18Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op18Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op18; }
	}

	public final Find_op18Context find_op18() throws RecognitionException {
		Find_op18Context _localctx = new Find_op18Context(_ctx, getState());
		enterRule(_localctx, 718, RULE_find_op18);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3935);
			match(T__166);
			setState(3936);
			((Find_op18Context)_localctx).File = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op7Context extends ParserRuleContext {
		public Grep_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op7; }
	}

	public final Grep_op7Context grep_op7() throws RecognitionException {
		Grep_op7Context _localctx = new Grep_op7Context(_ctx, getState());
		enterRule(_localctx, 720, RULE_grep_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3938);
			match(T__86);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Du_op7Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Du_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_du_op7; }
	}

	public final Du_op7Context du_op7() throws RecognitionException {
		Du_op7Context _localctx = new Du_op7Context(_ctx, getState());
		enterRule(_localctx, 722, RULE_du_op7);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3941); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3940);
				((Du_op7Context)_localctx).File = match(STRING);
				}
				}
				setState(3943); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op12Context extends ParserRuleContext {
		public Sort_op12Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op12; }
	}

	public final Sort_op12Context sort_op12() throws RecognitionException {
		Sort_op12Context _localctx = new Sort_op12Context(_ctx, getState());
		enterRule(_localctx, 724, RULE_sort_op12);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3945);
			match(T__38);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cp_op2Context extends ParserRuleContext {
		public Cp_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cp_op2; }
	}

	public final Cp_op2Context cp_op2() throws RecognitionException {
		Cp_op2Context _localctx = new Cp_op2Context(_ctx, getState());
		enterRule(_localctx, 726, RULE_cp_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3947);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op4Context extends ParserRuleContext {
		public Find_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op4; }
	}

	public final Find_op4Context find_op4() throws RecognitionException {
		Find_op4Context _localctx = new Find_op4Context(_ctx, getState());
		enterRule(_localctx, 728, RULE_find_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3949);
			match(T__38);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op19Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op19Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op19; }
	}

	public final Find_op19Context find_op19() throws RecognitionException {
		Find_op19Context _localctx = new Find_op19Context(_ctx, getState());
		enterRule(_localctx, 730, RULE_find_op19);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3951);
			match(T__167);
			setState(3952);
			((Find_op19Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op27Context extends ParserRuleContext {
		public Ls_op27Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op27; }
	}

	public final Ls_op27Context ls_op27() throws RecognitionException {
		Ls_op27Context _localctx = new Ls_op27Context(_ctx, getState());
		enterRule(_localctx, 732, RULE_ls_op27);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3954);
			match(T__43);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op2Context extends ParserRuleContext {
		public Zip_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op2; }
	}

	public final Zip_op2Context zip_op2() throws RecognitionException {
		Zip_op2Context _localctx = new Zip_op2Context(_ctx, getState());
		enterRule(_localctx, 734, RULE_zip_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3956);
			match(T__120);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op40Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Zip_op40Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op40; }
	}

	public final Zip_op40Context zip_op40() throws RecognitionException {
		Zip_op40Context _localctx = new Zip_op40Context(_ctx, getState());
		enterRule(_localctx, 736, RULE_zip_op40);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3958);
			match(T__168);
			setState(3959);
			((Zip_op40Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Du_op4Context extends ParserRuleContext {
		public Du_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_du_op4; }
	}

	public final Du_op4Context du_op4() throws RecognitionException {
		Du_op4Context _localctx = new Du_op4Context(_ctx, getState());
		enterRule(_localctx, 738, RULE_du_op4);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3961);
			_la = _input.LA(1);
			if ( !(((((_la - 37)) & ~0x3f) == 0 && ((1L << (_la - 37)) & ((1L << (T__36 - 37)) | (1L << (T__37 - 37)) | (1L << (T__64 - 37)) | (1L << (T__94 - 37)))) != 0)) ) {
			_errHandler.recoverInline(this);
			} else {
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op80Context extends ParserRuleContext {
		public Find_op80Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op80; }
	}

	public final Find_op80Context find_op80() throws RecognitionException {
		Find_op80Context _localctx = new Find_op80Context(_ctx, getState());
		enterRule(_localctx, 740, RULE_find_op80);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3963);
			match(T__169);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op45Context extends ParserRuleContext {
		public Tar_op45Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op45; }
	}

	public final Tar_op45Context tar_op45() throws RecognitionException {
		Tar_op45Context _localctx = new Tar_op45Context(_ctx, getState());
		enterRule(_localctx, 742, RULE_tar_op45);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3965);
			match(T__95);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op26Context extends ParserRuleContext {
		public Grep_op26Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op26; }
	}

	public final Grep_op26Context grep_op26() throws RecognitionException {
		Grep_op26Context _localctx = new Grep_op26Context(_ctx, getState());
		enterRule(_localctx, 744, RULE_grep_op26);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3967);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sed_op3Context extends ParserRuleContext {
		public Sed_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sed_op3; }
	}

	public final Sed_op3Context sed_op3() throws RecognitionException {
		Sed_op3Context _localctx = new Sed_op3Context(_ctx, getState());
		enterRule(_localctx, 746, RULE_sed_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3969);
			match(T__43);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op4Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Xargs_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op4; }
	}

	public final Xargs_op4Context xargs_op4() throws RecognitionException {
		Xargs_op4Context _localctx = new Xargs_op4Context(_ctx, getState());
		enterRule(_localctx, 748, RULE_xargs_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3971);
			match(T__91);
			setState(3972);
			((Xargs_op4Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op7Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Xargs_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op7; }
	}

	public final Xargs_op7Context xargs_op7() throws RecognitionException {
		Xargs_op7Context _localctx = new Xargs_op7Context(_ctx, getState());
		enterRule(_localctx, 750, RULE_xargs_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3974);
			match(T__61);
			setState(3975);
			((Xargs_op7Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op32Context extends ParserRuleContext {
		public Zip_op32Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op32; }
	}

	public final Zip_op32Context zip_op32() throws RecognitionException {
		Zip_op32Context _localctx = new Zip_op32Context(_ctx, getState());
		enterRule(_localctx, 752, RULE_zip_op32);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3977);
			match(T__170);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op15Context extends ParserRuleContext {
		public Token Time;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op15Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op15; }
	}

	public final Tar_op15Context tar_op15() throws RecognitionException {
		Tar_op15Context _localctx = new Tar_op15Context(_ctx, getState());
		enterRule(_localctx, 754, RULE_tar_op15);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3979);
			match(T__171);
			setState(3980);
			((Tar_op15Context)_localctx).Time = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op10Context extends ParserRuleContext {
		public Grep_op10Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op10; }
	}

	public final Grep_op10Context grep_op10() throws RecognitionException {
		Grep_op10Context _localctx = new Grep_op10Context(_ctx, getState());
		enterRule(_localctx, 756, RULE_grep_op10);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3982);
			match(T__103);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op3Context extends ParserRuleContext {
		public Egrep_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op3; }
	}

	public final Egrep_op3Context egrep_op3() throws RecognitionException {
		Egrep_op3Context _localctx = new Egrep_op3Context(_ctx, getState());
		enterRule(_localctx, 758, RULE_egrep_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3984);
			match(T__57);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op35Context extends ParserRuleContext {
		public Ls_op35Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op35; }
	}

	public final Ls_op35Context ls_op35() throws RecognitionException {
		Ls_op35Context _localctx = new Ls_op35Context(_ctx, getState());
		enterRule(_localctx, 760, RULE_ls_op35);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3986);
			match(T__41);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op23Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Tar_op23Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op23; }
	}

	public final Tar_op23Context tar_op23() throws RecognitionException {
		Tar_op23Context _localctx = new Tar_op23Context(_ctx, getState());
		enterRule(_localctx, 762, RULE_tar_op23);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3988);
			match(T__38);
			setState(3989);
			((Tar_op23Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op5Context extends ParserRuleContext {
		public Find_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op5; }
	}

	public final Find_op5Context find_op5() throws RecognitionException {
		Find_op5Context _localctx = new Find_op5Context(_ctx, getState());
		enterRule(_localctx, 764, RULE_find_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3991);
			match(T__13);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op23Context extends ParserRuleContext {
		public Egrep_op23Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op23; }
	}

	public final Egrep_op23Context egrep_op23() throws RecognitionException {
		Egrep_op23Context _localctx = new Egrep_op23Context(_ctx, getState());
		enterRule(_localctx, 766, RULE_egrep_op23);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3993);
			match(T__38);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op32Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Egrep_op32Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op32; }
	}

	public final Egrep_op32Context egrep_op32() throws RecognitionException {
		Egrep_op32Context _localctx = new Egrep_op32Context(_ctx, getState());
		enterRule(_localctx, 768, RULE_egrep_op32);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3995);
			match(T__60);
			setState(3996);
			((Egrep_op32Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Awk_op5Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Awk_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_awk_op5; }
	}

	public final Awk_op5Context awk_op5() throws RecognitionException {
		Awk_op5Context _localctx = new Awk_op5Context(_ctx, getState());
		enterRule(_localctx, 770, RULE_awk_op5);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(3999); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(3998);
				((Awk_op5Context)_localctx).File = match(STRING);
				}
				}
				setState(4001); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op16Context extends ParserRuleContext {
		public Sort_op16Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op16; }
	}

	public final Sort_op16Context sort_op16() throws RecognitionException {
		Sort_op16Context _localctx = new Sort_op16Context(_ctx, getState());
		enterRule(_localctx, 772, RULE_sort_op16);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4003);
			match(T__11);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op23Context extends ParserRuleContext {
		public Find_op23Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op23; }
	}

	public final Find_op23Context find_op23() throws RecognitionException {
		Find_op23Context _localctx = new Find_op23Context(_ctx, getState());
		enterRule(_localctx, 774, RULE_find_op23);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4005);
			match(T__10);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Seq_op2Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Seq_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_seq_op2; }
	}

	public final Seq_op2Context seq_op2() throws RecognitionException {
		Seq_op2Context _localctx = new Seq_op2Context(_ctx, getState());
		enterRule(_localctx, 776, RULE_seq_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4007);
			match(T__38);
			setState(4008);
			((Seq_op2Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op1Context extends ParserRuleContext {
		public Find_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op1; }
	}

	public final Find_op1Context find_op1() throws RecognitionException {
		Find_op1Context _localctx = new Find_op1Context(_ctx, getState());
		enterRule(_localctx, 778, RULE_find_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4010);
			match(T__91);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op39Context extends ParserRuleContext {
		public Token File;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Zip_op38Context zip_op38() {
			return getRuleContext(Zip_op38Context.class,0);
		}
		public Zip_op39Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op39; }
	}

	public final Zip_op39Context zip_op39() throws RecognitionException {
		Zip_op39Context _localctx = new Zip_op39Context(_ctx, getState());
		enterRule(_localctx, 780, RULE_zip_op39);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4012);
			((Zip_op39Context)_localctx).File = match(STRING);
			setState(4014);
			_la = _input.LA(1);
			if (_la==STRING) {
				{
				setState(4013);
				zip_op38();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sh_op0Context extends ParserRuleContext {
		public Token String;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Sh_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sh_op0; }
	}

	public final Sh_op0Context sh_op0() throws RecognitionException {
		Sh_op0Context _localctx = new Sh_op0Context(_ctx, getState());
		enterRule(_localctx, 782, RULE_sh_op0);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(4017); 
			_errHandler.sync(this);
			_alt = 1;
			do {
				switch (_alt) {
				case 1:
					{
					{
					setState(4016);
					((Sh_op0Context)_localctx).String = match(STRING);
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(4019); 
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,711,_ctx);
			} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op3Context extends ParserRuleContext {
		public Sort_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op3; }
	}

	public final Sort_op3Context sort_op3() throws RecognitionException {
		Sort_op3Context _localctx = new Sort_op3Context(_ctx, getState());
		enterRule(_localctx, 784, RULE_sort_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4021);
			match(T__37);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op9Context extends ParserRuleContext {
		public Ls_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op9; }
	}

	public final Ls_op9Context ls_op9() throws RecognitionException {
		Ls_op9Context _localctx = new Ls_op9Context(_ctx, getState());
		enterRule(_localctx, 786, RULE_ls_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4023);
			match(T__89);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op1Context extends ParserRuleContext {
		public Ls_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op1; }
	}

	public final Ls_op1Context ls_op1() throws RecognitionException {
		Ls_op1Context _localctx = new Ls_op1Context(_ctx, getState());
		enterRule(_localctx, 788, RULE_ls_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4025);
			match(T__120);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op78Context extends ParserRuleContext {
		public Token String;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op78Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op78; }
	}

	public final Find_op78Context find_op78() throws RecognitionException {
		Find_op78Context _localctx = new Find_op78Context(_ctx, getState());
		enterRule(_localctx, 790, RULE_find_op78);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4027);
			match(T__172);
			setState(4028);
			((Find_op78Context)_localctx).String = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op31Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Grep_op31Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op31; }
	}

	public final Grep_op31Context grep_op31() throws RecognitionException {
		Grep_op31Context _localctx = new Grep_op31Context(_ctx, getState());
		enterRule(_localctx, 792, RULE_grep_op31);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4030);
			match(T__120);
			setState(4031);
			((Grep_op31Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op6Context extends ParserRuleContext {
		public Ls_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op6; }
	}

	public final Ls_op6Context ls_op6() throws RecognitionException {
		Ls_op6Context _localctx = new Ls_op6Context(_ctx, getState());
		enterRule(_localctx, 794, RULE_ls_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4033);
			match(T__83);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sed_op4Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Sed_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sed_op4; }
	}

	public final Sed_op4Context sed_op4() throws RecognitionException {
		Sed_op4Context _localctx = new Sed_op4Context(_ctx, getState());
		enterRule(_localctx, 796, RULE_sed_op4);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4036); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(4035);
				((Sed_op4Context)_localctx).File = match(STRING);
				}
				}
				setState(4038); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cd_op0Context extends ParserRuleContext {
		public Cd_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cd_op0; }
	}

	public final Cd_op0Context cd_op0() throws RecognitionException {
		Cd_op0Context _localctx = new Cd_op0Context(_ctx, getState());
		enterRule(_localctx, 798, RULE_cd_op0);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4040);
			_la = _input.LA(1);
			if ( !(_la==T__56 || _la==T__83) ) {
			_errHandler.recoverInline(this);
			} else {
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op21Context extends ParserRuleContext {
		public Grep_op21Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op21; }
	}

	public final Grep_op21Context grep_op21() throws RecognitionException {
		Grep_op21Context _localctx = new Grep_op21Context(_ctx, getState());
		enterRule(_localctx, 800, RULE_grep_op21);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4042);
			match(T__89);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op37Context extends ParserRuleContext {
		public Egrep_op37Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op37; }
	}

	public final Egrep_op37Context egrep_op37() throws RecognitionException {
		Egrep_op37Context _localctx = new Egrep_op37Context(_ctx, getState());
		enterRule(_localctx, 802, RULE_egrep_op37);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4044);
			match(T__110);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op46Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op46Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op46; }
	}

	public final Find_op46Context find_op46() throws RecognitionException {
		Find_op46Context _localctx = new Find_op46Context(_ctx, getState());
		enterRule(_localctx, 804, RULE_find_op46);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4046);
			match(T__173);
			setState(4047);
			((Find_op46Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op34Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Tar_op34Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op34; }
	}

	public final Tar_op34Context tar_op34() throws RecognitionException {
		Tar_op34Context _localctx = new Tar_op34Context(_ctx, getState());
		enterRule(_localctx, 806, RULE_tar_op34);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4050); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(4049);
				((Tar_op34Context)_localctx).File = match(STRING);
				}
				}
				setState(4052); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op30Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Egrep_op30Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op30; }
	}

	public final Egrep_op30Context egrep_op30() throws RecognitionException {
		Egrep_op30Context _localctx = new Egrep_op30Context(_ctx, getState());
		enterRule(_localctx, 808, RULE_egrep_op30);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4054);
			match(T__63);
			setState(4055);
			((Egrep_op30Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op9Context extends ParserRuleContext {
		public Egrep_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op9; }
	}

	public final Egrep_op9Context egrep_op9() throws RecognitionException {
		Egrep_op9Context _localctx = new Egrep_op9Context(_ctx, getState());
		enterRule(_localctx, 810, RULE_egrep_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4057);
			match(T__94);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chown_op2Context extends ParserRuleContext {
		public Chown_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chown_op2; }
	}

	public final Chown_op2Context chown_op2() throws RecognitionException {
		Chown_op2Context _localctx = new Chown_op2Context(_ctx, getState());
		enterRule(_localctx, 812, RULE_chown_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4059);
			match(T__49);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Diff_op0Context extends ParserRuleContext {
		public Token String;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Diff_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_diff_op0; }
	}

	public final Diff_op0Context diff_op0() throws RecognitionException {
		Diff_op0Context _localctx = new Diff_op0Context(_ctx, getState());
		enterRule(_localctx, 814, RULE_diff_op0);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(4062); 
			_errHandler.sync(this);
			_alt = 1;
			do {
				switch (_alt) {
				case 1:
					{
					{
					setState(4061);
					((Diff_op0Context)_localctx).String = match(STRING);
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(4064); 
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,714,_ctx);
			} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op8Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Xargs_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op8; }
	}

	public final Xargs_op8Context xargs_op8() throws RecognitionException {
		Xargs_op8Context _localctx = new Xargs_op8Context(_ctx, getState());
		enterRule(_localctx, 816, RULE_xargs_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4066);
			match(T__83);
			setState(4067);
			((Xargs_op8Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Sort_op8Context extends ParserRuleContext {
		public Sort_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sort_op8; }
	}

	public final Sort_op8Context sort_op8() throws RecognitionException {
		Sort_op8Context _localctx = new Sort_op8Context(_ctx, getState());
		enterRule(_localctx, 818, RULE_sort_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4069);
			match(T__9);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op6Context extends ParserRuleContext {
		public Tar_op6Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op6; }
	}

	public final Tar_op6Context tar_op6() throws RecognitionException {
		Tar_op6Context _localctx = new Tar_op6Context(_ctx, getState());
		enterRule(_localctx, 820, RULE_tar_op6);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4071);
			match(T__82);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op13Context extends ParserRuleContext {
		public Ls_op13Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op13; }
	}

	public final Ls_op13Context ls_op13() throws RecognitionException {
		Ls_op13Context _localctx = new Ls_op13Context(_ctx, getState());
		enterRule(_localctx, 822, RULE_ls_op13);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4073);
			match(T__111);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op0Context extends ParserRuleContext {
		public Unzip_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op0; }
	}

	public final Unzip_op0Context unzip_op0() throws RecognitionException {
		Unzip_op0Context _localctx = new Unzip_op0Context(_ctx, getState());
		enterRule(_localctx, 824, RULE_unzip_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4075);
			match(T__71);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op19Context extends ParserRuleContext {
		public Egrep_op19Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op19; }
	}

	public final Egrep_op19Context egrep_op19() throws RecognitionException {
		Egrep_op19Context _localctx = new Egrep_op19Context(_ctx, getState());
		enterRule(_localctx, 826, RULE_egrep_op19);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4077);
			match(T__95);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op14Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op14Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op14; }
	}

	public final Find_op14Context find_op14() throws RecognitionException {
		Find_op14Context _localctx = new Find_op14Context(_ctx, getState());
		enterRule(_localctx, 828, RULE_find_op14);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4079);
			match(T__174);
			setState(4080);
			((Find_op14Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op62Context extends ParserRuleContext {
		public Token Utility;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op28Context find_op28() {
			return getRuleContext(Find_op28Context.class,0);
		}
		public Find_op62Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op62; }
	}

	public final Find_op62Context find_op62() throws RecognitionException {
		Find_op62Context _localctx = new Find_op62Context(_ctx, getState());
		enterRule(_localctx, 830, RULE_find_op62);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4082);
			match(T__175);
			setState(4083);
			((Find_op62Context)_localctx).Utility = match(STRING);
			setState(4085);
			_la = _input.LA(1);
			if (_la==STRING) {
				{
				setState(4084);
				find_op28();
				}
			}

			setState(4087);
			match(T__73);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op38Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Ls_op38Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op38; }
	}

	public final Ls_op38Context ls_op38() throws RecognitionException {
		Ls_op38Context _localctx = new Ls_op38Context(_ctx, getState());
		enterRule(_localctx, 832, RULE_ls_op38);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4090); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(4089);
				((Ls_op38Context)_localctx).File = match(STRING);
				}
				}
				setState(4092); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chown_op0Context extends ParserRuleContext {
		public Chown_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chown_op0; }
	}

	public final Chown_op0Context chown_op0() throws RecognitionException {
		Chown_op0Context _localctx = new Chown_op0Context(_ctx, getState());
		enterRule(_localctx, 834, RULE_chown_op0);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4094);
			match(T__1);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op20Context extends ParserRuleContext {
		public Find_op20Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op20; }
	}

	public final Find_op20Context find_op20() throws RecognitionException {
		Find_op20Context _localctx = new Find_op20Context(_ctx, getState());
		enterRule(_localctx, 836, RULE_find_op20);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4096);
			match(T__51);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op11Context extends ParserRuleContext {
		public Zip_op11Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op11; }
	}

	public final Zip_op11Context zip_op11() throws RecognitionException {
		Zip_op11Context _localctx = new Zip_op11Context(_ctx, getState());
		enterRule(_localctx, 838, RULE_zip_op11);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4098);
			match(T__94);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op8Context extends ParserRuleContext {
		public Egrep_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op8; }
	}

	public final Egrep_op8Context egrep_op8() throws RecognitionException {
		Egrep_op8Context _localctx = new Egrep_op8Context(_ctx, getState());
		enterRule(_localctx, 840, RULE_egrep_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4100);
			match(T__82);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chmod_op10Context extends ParserRuleContext {
		public Chmod_op10Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chmod_op10; }
	}

	public final Chmod_op10Context chmod_op10() throws RecognitionException {
		Chmod_op10Context _localctx = new Chmod_op10Context(_ctx, getState());
		enterRule(_localctx, 842, RULE_chmod_op10);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4102);
			match(T__60);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op28Context extends ParserRuleContext {
		public Egrep_op28Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op28; }
	}

	public final Egrep_op28Context egrep_op28() throws RecognitionException {
		Egrep_op28Context _localctx = new Egrep_op28Context(_ctx, getState());
		enterRule(_localctx, 844, RULE_egrep_op28);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4104);
			match(T__13);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op29Context extends ParserRuleContext {
		public Zip_op29Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op29; }
	}

	public final Zip_op29Context zip_op29() throws RecognitionException {
		Zip_op29Context _localctx = new Zip_op29Context(_ctx, getState());
		enterRule(_localctx, 846, RULE_zip_op29);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4106);
			match(T__127);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op4Context extends ParserRuleContext {
		public Egrep_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op4; }
	}

	public final Egrep_op4Context egrep_op4() throws RecognitionException {
		Egrep_op4Context _localctx = new Egrep_op4Context(_ctx, getState());
		enterRule(_localctx, 848, RULE_egrep_op4);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4108);
			match(T__139);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op3Context extends ParserRuleContext {
		public Zip_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op3; }
	}

	public final Zip_op3Context zip_op3() throws RecognitionException {
		Zip_op3Context _localctx = new Zip_op3Context(_ctx, getState());
		enterRule(_localctx, 850, RULE_zip_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4110);
			match(T__9);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op17Context extends ParserRuleContext {
		public Ls_op17Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op17; }
	}

	public final Ls_op17Context ls_op17() throws RecognitionException {
		Ls_op17Context _localctx = new Ls_op17Context(_ctx, getState());
		enterRule(_localctx, 852, RULE_ls_op17);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4112);
			match(T__9);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op21Context extends ParserRuleContext {
		public Find_op21Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op21; }
	}

	public final Find_op21Context find_op21() throws RecognitionException {
		Find_op21Context _localctx = new Find_op21Context(_ctx, getState());
		enterRule(_localctx, 854, RULE_find_op21);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4114);
			match(T__116);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op3Context extends ParserRuleContext {
		public Grep_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op3; }
	}

	public final Grep_op3Context grep_op3() throws RecognitionException {
		Grep_op3Context _localctx = new Grep_op3Context(_ctx, getState());
		enterRule(_localctx, 856, RULE_grep_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4116);
			match(T__57);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op7Context extends ParserRuleContext {
		public Unzip_op7Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op7; }
	}

	public final Unzip_op7Context unzip_op7() throws RecognitionException {
		Unzip_op7Context _localctx = new Unzip_op7Context(_ctx, getState());
		enterRule(_localctx, 858, RULE_unzip_op7);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4118);
			match(T__11);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op8Context extends ParserRuleContext {
		public Grep_op8Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op8; }
	}

	public final Grep_op8Context grep_op8() throws RecognitionException {
		Grep_op8Context _localctx = new Grep_op8Context(_ctx, getState());
		enterRule(_localctx, 860, RULE_grep_op8);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4120);
			match(T__82);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op41Context extends ParserRuleContext {
		public Tar_op41Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op41; }
	}

	public final Tar_op41Context tar_op41() throws RecognitionException {
		Tar_op41Context _localctx = new Tar_op41Context(_ctx, getState());
		enterRule(_localctx, 862, RULE_tar_op41);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4122);
			match(T__64);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cp_op9Context extends ParserRuleContext {
		public Cp_op9Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cp_op9; }
	}

	public final Cp_op9Context cp_op9() throws RecognitionException {
		Cp_op9Context _localctx = new Cp_op9Context(_ctx, getState());
		enterRule(_localctx, 864, RULE_cp_op9);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4124);
			match(T__74);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Cat_op5Context extends ParserRuleContext {
		public Cat_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_cat_op5; }
	}

	public final Cat_op5Context cat_op5() throws RecognitionException {
		Cat_op5Context _localctx = new Cat_op5Context(_ctx, getState());
		enterRule(_localctx, 866, RULE_cat_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4126);
			match(T__11);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op20Context extends ParserRuleContext {
		public Zip_op20Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op20; }
	}

	public final Zip_op20Context zip_op20() throws RecognitionException {
		Zip_op20Context _localctx = new Zip_op20Context(_ctx, getState());
		enterRule(_localctx, 868, RULE_zip_op20);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4128);
			match(T__89);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op40Context extends ParserRuleContext {
		public Token File;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Egrep_op40Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op40; }
	}

	public final Egrep_op40Context egrep_op40() throws RecognitionException {
		Egrep_op40Context _localctx = new Egrep_op40Context(_ctx, getState());
		enterRule(_localctx, 870, RULE_egrep_op40);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4131); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(4130);
				((Egrep_op40Context)_localctx).File = match(STRING);
				}
				}
				setState(4133); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==STRING );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Zip_op15Context extends ParserRuleContext {
		public Zip_op15Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_zip_op15; }
	}

	public final Zip_op15Context zip_op15() throws RecognitionException {
		Zip_op15Context _localctx = new Zip_op15Context(_ctx, getState());
		enterRule(_localctx, 872, RULE_zip_op15);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4135);
			match(T__83);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op12Context extends ParserRuleContext {
		public Unzip_op12Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op12; }
	}

	public final Unzip_op12Context unzip_op12() throws RecognitionException {
		Unzip_op12Context _localctx = new Unzip_op12Context(_ctx, getState());
		enterRule(_localctx, 874, RULE_unzip_op12);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4137);
			match(T__53);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op30Context extends ParserRuleContext {
		public Token Utility;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op28Context find_op28() {
			return getRuleContext(Find_op28Context.class,0);
		}
		public Find_op30Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op30; }
	}

	public final Find_op30Context find_op30() throws RecognitionException {
		Find_op30Context _localctx = new Find_op30Context(_ctx, getState());
		enterRule(_localctx, 876, RULE_find_op30);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4139);
			match(T__176);
			setState(4140);
			((Find_op30Context)_localctx).Utility = match(STRING);
			setState(4142);
			_la = _input.LA(1);
			if (_la==STRING) {
				{
				setState(4141);
				find_op28();
				}
			}

			setState(4145); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(4144);
				match(T__177);
				}
				}
				setState(4147); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==T__177 );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op26Context extends ParserRuleContext {
		public Ls_op26Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op26; }
	}

	public final Ls_op26Context ls_op26() throws RecognitionException {
		Ls_op26Context _localctx = new Ls_op26Context(_ctx, getState());
		enterRule(_localctx, 878, RULE_ls_op26);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4149);
			match(T__36);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op3Context extends ParserRuleContext {
		public Unzip_op3Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op3; }
	}

	public final Unzip_op3Context unzip_op3() throws RecognitionException {
		Unzip_op3Context _localctx = new Unzip_op3Context(_ctx, getState());
		enterRule(_localctx, 880, RULE_unzip_op3);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4151);
			match(T__78);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op28Context extends ParserRuleContext {
		public Tar_op28Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op28; }
	}

	public final Tar_op28Context tar_op28() throws RecognitionException {
		Tar_op28Context _localctx = new Tar_op28Context(_ctx, getState());
		enterRule(_localctx, 882, RULE_tar_op28);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4153);
			match(T__41);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Chown_op4Context extends ParserRuleContext {
		public Chown_op3Context chown_op3() {
			return getRuleContext(Chown_op3Context.class,0);
		}
		public Chown_op4Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chown_op4; }
	}

	public final Chown_op4Context chown_op4() throws RecognitionException {
		Chown_op4Context _localctx = new Chown_op4Context(_ctx, getState());
		enterRule(_localctx, 884, RULE_chown_op4);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4155);
			match(T__89);
			setState(4157);
			_la = _input.LA(1);
			if (((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) {
				{
				setState(4156);
				chown_op3();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op22Context extends ParserRuleContext {
		public Find_op22Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op22; }
	}

	public final Find_op22Context find_op22() throws RecognitionException {
		Find_op22Context _localctx = new Find_op22Context(_ctx, getState());
		enterRule(_localctx, 886, RULE_find_op22);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4159);
			match(T__12);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Head_op1Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Head_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_head_op1; }
	}

	public final Head_op1Context head_op1() throws RecognitionException {
		Head_op1Context _localctx = new Head_op1Context(_ctx, getState());
		enterRule(_localctx, 888, RULE_head_op1);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4161);
			match(T__9);
			setState(4162);
			((Head_op1Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Rm_op5Context extends ParserRuleContext {
		public Rm_op5Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rm_op5; }
	}

	public final Rm_op5Context rm_op5() throws RecognitionException {
		Rm_op5Context _localctx = new Rm_op5Context(_ctx, getState());
		enterRule(_localctx, 890, RULE_rm_op5);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4164);
			match(T__10);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op21Context extends ParserRuleContext {
		public Unzip_op21Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op21; }
	}

	public final Unzip_op21Context unzip_op21() throws RecognitionException {
		Unzip_op21Context _localctx = new Unzip_op21Context(_ctx, getState());
		enterRule(_localctx, 892, RULE_unzip_op21);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4166);
			match(T__115);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op26Context extends ParserRuleContext {
		public Token Number;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op26Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op26; }
	}

	public final Find_op26Context find_op26() throws RecognitionException {
		Find_op26Context _localctx = new Find_op26Context(_ctx, getState());
		enterRule(_localctx, 894, RULE_find_op26);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4168);
			match(T__80);
			setState(4169);
			((Find_op26Context)_localctx).Number = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Awk_op2Context extends ParserRuleContext {
		public Token String;
		public List<TerminalNode> STRING() { return getTokens(CommandsParser.STRING); }
		public TerminalNode STRING(int i) {
			return getToken(CommandsParser.STRING, i);
		}
		public Awk_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_awk_op2; }
	}

	public final Awk_op2Context awk_op2() throws RecognitionException {
		Awk_op2Context _localctx = new Awk_op2Context(_ctx, getState());
		enterRule(_localctx, 896, RULE_awk_op2);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(4172); 
			_errHandler.sync(this);
			_alt = 1;
			do {
				switch (_alt) {
				case 1:
					{
					{
					setState(4171);
					((Awk_op2Context)_localctx).String = match(STRING);
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(4174); 
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,721,_ctx);
			} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op33Context extends ParserRuleContext {
		public Token Pattern;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Egrep_op33Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op33; }
	}

	public final Egrep_op33Context egrep_op33() throws RecognitionException {
		Egrep_op33Context _localctx = new Egrep_op33Context(_ctx, getState());
		enterRule(_localctx, 898, RULE_egrep_op33);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4176);
			match(T__85);
			setState(4177);
			((Egrep_op33Context)_localctx).Pattern = match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op25Context extends ParserRuleContext {
		public Grep_op25Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op25; }
	}

	public final Grep_op25Context grep_op25() throws RecognitionException {
		Grep_op25Context _localctx = new Grep_op25Context(_ctx, getState());
		enterRule(_localctx, 900, RULE_grep_op25);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4179);
			match(T__115);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Unzip_op16Context extends ParserRuleContext {
		public Unzip_op16Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unzip_op16; }
	}

	public final Unzip_op16Context unzip_op16() throws RecognitionException {
		Unzip_op16Context _localctx = new Unzip_op16Context(_ctx, getState());
		enterRule(_localctx, 902, RULE_unzip_op16);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4181);
			match(T__38);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Du_op0Context extends ParserRuleContext {
		public Du_op0Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_du_op0; }
	}

	public final Du_op0Context du_op0() throws RecognitionException {
		Du_op0Context _localctx = new Du_op0Context(_ctx, getState());
		enterRule(_localctx, 904, RULE_du_op0);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4183);
			_la = _input.LA(1);
			if ( !(((((_la - 57)) & ~0x3f) == 0 && ((1L << (_la - 57)) & ((1L << (T__56 - 57)) | (1L << (T__82 - 57)) | (1L << (T__83 - 57)))) != 0)) ) {
			_errHandler.recoverInline(this);
			} else {
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Xargs_op14Context extends ParserRuleContext {
		public Token Utility;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Xargs_op13Context xargs_op13() {
			return getRuleContext(Xargs_op13Context.class,0);
		}
		public Xargs_op14Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_xargs_op14; }
	}

	public final Xargs_op14Context xargs_op14() throws RecognitionException {
		Xargs_op14Context _localctx = new Xargs_op14Context(_ctx, getState());
		enterRule(_localctx, 906, RULE_xargs_op14);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4185);
			((Xargs_op14Context)_localctx).Utility = match(STRING);
			setState(4187);
			_la = _input.LA(1);
			if (_la==STRING) {
				{
				setState(4186);
				xargs_op13();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Find_op29Context extends ParserRuleContext {
		public Token Utility;
		public TerminalNode STRING() { return getToken(CommandsParser.STRING, 0); }
		public Find_op28Context find_op28() {
			return getRuleContext(Find_op28Context.class,0);
		}
		public Find_op29Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_find_op29; }
	}

	public final Find_op29Context find_op29() throws RecognitionException {
		Find_op29Context _localctx = new Find_op29Context(_ctx, getState());
		enterRule(_localctx, 908, RULE_find_op29);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4189);
			match(T__176);
			setState(4190);
			((Find_op29Context)_localctx).Utility = match(STRING);
			setState(4192);
			_la = _input.LA(1);
			if (_la==STRING) {
				{
				setState(4191);
				find_op28();
				}
			}

			setState(4194);
			match(T__73);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Tar_op13Context extends ParserRuleContext {
		public Tar_op13Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tar_op13; }
	}

	public final Tar_op13Context tar_op13() throws RecognitionException {
		Tar_op13Context _localctx = new Tar_op13Context(_ctx, getState());
		enterRule(_localctx, 910, RULE_tar_op13);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4196);
			match(T__43);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Grep_op11Context extends ParserRuleContext {
		public Grep_op11Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_grep_op11; }
	}

	public final Grep_op11Context grep_op11() throws RecognitionException {
		Grep_op11Context _localctx = new Grep_op11Context(_ctx, getState());
		enterRule(_localctx, 912, RULE_grep_op11);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4198);
			match(T__84);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op36Context extends ParserRuleContext {
		public Egrep_op36Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op36; }
	}

	public final Egrep_op36Context egrep_op36() throws RecognitionException {
		Egrep_op36Context _localctx = new Egrep_op36Context(_ctx, getState());
		enterRule(_localctx, 914, RULE_egrep_op36);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4200);
			match(T__75);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Egrep_op14Context extends ParserRuleContext {
		public Egrep_op14Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_egrep_op14; }
	}

	public final Egrep_op14Context egrep_op14() throws RecognitionException {
		Egrep_op14Context _localctx = new Egrep_op14Context(_ctx, getState());
		enterRule(_localctx, 916, RULE_egrep_op14);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4202);
			match(T__78);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Ls_op31Context extends ParserRuleContext {
		public Ls_op31Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ls_op31; }
	}

	public final Ls_op31Context ls_op31() throws RecognitionException {
		Ls_op31Context _localctx = new Ls_op31Context(_ctx, getState());
		enterRule(_localctx, 918, RULE_ls_op31);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4204);
			match(T__10);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	private static final int _serializedATNSegments = 2;
	private static final String _serializedATNSegment0 =
		"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\u00b6\u1071\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4"+
		",\t,\4-\t-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64\t"+
		"\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:\4;\t;\4<\t<\4=\t="+
		"\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\tC\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I"+
		"\tI\4J\tJ\4K\tK\4L\tL\4M\tM\4N\tN\4O\tO\4P\tP\4Q\tQ\4R\tR\4S\tS\4T\tT"+
		"\4U\tU\4V\tV\4W\tW\4X\tX\4Y\tY\4Z\tZ\4[\t[\4\\\t\\\4]\t]\4^\t^\4_\t_\4"+
		"`\t`\4a\ta\4b\tb\4c\tc\4d\td\4e\te\4f\tf\4g\tg\4h\th\4i\ti\4j\tj\4k\t"+
		"k\4l\tl\4m\tm\4n\tn\4o\to\4p\tp\4q\tq\4r\tr\4s\ts\4t\tt\4u\tu\4v\tv\4"+
		"w\tw\4x\tx\4y\ty\4z\tz\4{\t{\4|\t|\4}\t}\4~\t~\4\177\t\177\4\u0080\t\u0080"+
		"\4\u0081\t\u0081\4\u0082\t\u0082\4\u0083\t\u0083\4\u0084\t\u0084\4\u0085"+
		"\t\u0085\4\u0086\t\u0086\4\u0087\t\u0087\4\u0088\t\u0088\4\u0089\t\u0089"+
		"\4\u008a\t\u008a\4\u008b\t\u008b\4\u008c\t\u008c\4\u008d\t\u008d\4\u008e"+
		"\t\u008e\4\u008f\t\u008f\4\u0090\t\u0090\4\u0091\t\u0091\4\u0092\t\u0092"+
		"\4\u0093\t\u0093\4\u0094\t\u0094\4\u0095\t\u0095\4\u0096\t\u0096\4\u0097"+
		"\t\u0097\4\u0098\t\u0098\4\u0099\t\u0099\4\u009a\t\u009a\4\u009b\t\u009b"+
		"\4\u009c\t\u009c\4\u009d\t\u009d\4\u009e\t\u009e\4\u009f\t\u009f\4\u00a0"+
		"\t\u00a0\4\u00a1\t\u00a1\4\u00a2\t\u00a2\4\u00a3\t\u00a3\4\u00a4\t\u00a4"+
		"\4\u00a5\t\u00a5\4\u00a6\t\u00a6\4\u00a7\t\u00a7\4\u00a8\t\u00a8\4\u00a9"+
		"\t\u00a9\4\u00aa\t\u00aa\4\u00ab\t\u00ab\4\u00ac\t\u00ac\4\u00ad\t\u00ad"+
		"\4\u00ae\t\u00ae\4\u00af\t\u00af\4\u00b0\t\u00b0\4\u00b1\t\u00b1\4\u00b2"+
		"\t\u00b2\4\u00b3\t\u00b3\4\u00b4\t\u00b4\4\u00b5\t\u00b5\4\u00b6\t\u00b6"+
		"\4\u00b7\t\u00b7\4\u00b8\t\u00b8\4\u00b9\t\u00b9\4\u00ba\t\u00ba\4\u00bb"+
		"\t\u00bb\4\u00bc\t\u00bc\4\u00bd\t\u00bd\4\u00be\t\u00be\4\u00bf\t\u00bf"+
		"\4\u00c0\t\u00c0\4\u00c1\t\u00c1\4\u00c2\t\u00c2\4\u00c3\t\u00c3\4\u00c4"+
		"\t\u00c4\4\u00c5\t\u00c5\4\u00c6\t\u00c6\4\u00c7\t\u00c7\4\u00c8\t\u00c8"+
		"\4\u00c9\t\u00c9\4\u00ca\t\u00ca\4\u00cb\t\u00cb\4\u00cc\t\u00cc\4\u00cd"+
		"\t\u00cd\4\u00ce\t\u00ce\4\u00cf\t\u00cf\4\u00d0\t\u00d0\4\u00d1\t\u00d1"+
		"\4\u00d2\t\u00d2\4\u00d3\t\u00d3\4\u00d4\t\u00d4\4\u00d5\t\u00d5\4\u00d6"+
		"\t\u00d6\4\u00d7\t\u00d7\4\u00d8\t\u00d8\4\u00d9\t\u00d9\4\u00da\t\u00da"+
		"\4\u00db\t\u00db\4\u00dc\t\u00dc\4\u00dd\t\u00dd\4\u00de\t\u00de\4\u00df"+
		"\t\u00df\4\u00e0\t\u00e0\4\u00e1\t\u00e1\4\u00e2\t\u00e2\4\u00e3\t\u00e3"+
		"\4\u00e4\t\u00e4\4\u00e5\t\u00e5\4\u00e6\t\u00e6\4\u00e7\t\u00e7\4\u00e8"+
		"\t\u00e8\4\u00e9\t\u00e9\4\u00ea\t\u00ea\4\u00eb\t\u00eb\4\u00ec\t\u00ec"+
		"\4\u00ed\t\u00ed\4\u00ee\t\u00ee\4\u00ef\t\u00ef\4\u00f0\t\u00f0\4\u00f1"+
		"\t\u00f1\4\u00f2\t\u00f2\4\u00f3\t\u00f3\4\u00f4\t\u00f4\4\u00f5\t\u00f5"+
		"\4\u00f6\t\u00f6\4\u00f7\t\u00f7\4\u00f8\t\u00f8\4\u00f9\t\u00f9\4\u00fa"+
		"\t\u00fa\4\u00fb\t\u00fb\4\u00fc\t\u00fc\4\u00fd\t\u00fd\4\u00fe\t\u00fe"+
		"\4\u00ff\t\u00ff\4\u0100\t\u0100\4\u0101\t\u0101\4\u0102\t\u0102\4\u0103"+
		"\t\u0103\4\u0104\t\u0104\4\u0105\t\u0105\4\u0106\t\u0106\4\u0107\t\u0107"+
		"\4\u0108\t\u0108\4\u0109\t\u0109\4\u010a\t\u010a\4\u010b\t\u010b\4\u010c"+
		"\t\u010c\4\u010d\t\u010d\4\u010e\t\u010e\4\u010f\t\u010f\4\u0110\t\u0110"+
		"\4\u0111\t\u0111\4\u0112\t\u0112\4\u0113\t\u0113\4\u0114\t\u0114\4\u0115"+
		"\t\u0115\4\u0116\t\u0116\4\u0117\t\u0117\4\u0118\t\u0118\4\u0119\t\u0119"+
		"\4\u011a\t\u011a\4\u011b\t\u011b\4\u011c\t\u011c\4\u011d\t\u011d\4\u011e"+
		"\t\u011e\4\u011f\t\u011f\4\u0120\t\u0120\4\u0121\t\u0121\4\u0122\t\u0122"+
		"\4\u0123\t\u0123\4\u0124\t\u0124\4\u0125\t\u0125\4\u0126\t\u0126\4\u0127"+
		"\t\u0127\4\u0128\t\u0128\4\u0129\t\u0129\4\u012a\t\u012a\4\u012b\t\u012b"+
		"\4\u012c\t\u012c\4\u012d\t\u012d\4\u012e\t\u012e\4\u012f\t\u012f\4\u0130"+
		"\t\u0130\4\u0131\t\u0131\4\u0132\t\u0132\4\u0133\t\u0133\4\u0134\t\u0134"+
		"\4\u0135\t\u0135\4\u0136\t\u0136\4\u0137\t\u0137\4\u0138\t\u0138\4\u0139"+
		"\t\u0139\4\u013a\t\u013a\4\u013b\t\u013b\4\u013c\t\u013c\4\u013d\t\u013d"+
		"\4\u013e\t\u013e\4\u013f\t\u013f\4\u0140\t\u0140\4\u0141\t\u0141\4\u0142"+
		"\t\u0142\4\u0143\t\u0143\4\u0144\t\u0144\4\u0145\t\u0145\4\u0146\t\u0146"+
		"\4\u0147\t\u0147\4\u0148\t\u0148\4\u0149\t\u0149\4\u014a\t\u014a\4\u014b"+
		"\t\u014b\4\u014c\t\u014c\4\u014d\t\u014d\4\u014e\t\u014e\4\u014f\t\u014f"+
		"\4\u0150\t\u0150\4\u0151\t\u0151\4\u0152\t\u0152\4\u0153\t\u0153\4\u0154"+
		"\t\u0154\4\u0155\t\u0155\4\u0156\t\u0156\4\u0157\t\u0157\4\u0158\t\u0158"+
		"\4\u0159\t\u0159\4\u015a\t\u015a\4\u015b\t\u015b\4\u015c\t\u015c\4\u015d"+
		"\t\u015d\4\u015e\t\u015e\4\u015f\t\u015f\4\u0160\t\u0160\4\u0161\t\u0161"+
		"\4\u0162\t\u0162\4\u0163\t\u0163\4\u0164\t\u0164\4\u0165\t\u0165\4\u0166"+
		"\t\u0166\4\u0167\t\u0167\4\u0168\t\u0168\4\u0169\t\u0169\4\u016a\t\u016a"+
		"\4\u016b\t\u016b\4\u016c\t\u016c\4\u016d\t\u016d\4\u016e\t\u016e\4\u016f"+
		"\t\u016f\4\u0170\t\u0170\4\u0171\t\u0171\4\u0172\t\u0172\4\u0173\t\u0173"+
		"\4\u0174\t\u0174\4\u0175\t\u0175\4\u0176\t\u0176\4\u0177\t\u0177\4\u0178"+
		"\t\u0178\4\u0179\t\u0179\4\u017a\t\u017a\4\u017b\t\u017b\4\u017c\t\u017c"+
		"\4\u017d\t\u017d\4\u017e\t\u017e\4\u017f\t\u017f\4\u0180\t\u0180\4\u0181"+
		"\t\u0181\4\u0182\t\u0182\4\u0183\t\u0183\4\u0184\t\u0184\4\u0185\t\u0185"+
		"\4\u0186\t\u0186\4\u0187\t\u0187\4\u0188\t\u0188\4\u0189\t\u0189\4\u018a"+
		"\t\u018a\4\u018b\t\u018b\4\u018c\t\u018c\4\u018d\t\u018d\4\u018e\t\u018e"+
		"\4\u018f\t\u018f\4\u0190\t\u0190\4\u0191\t\u0191\4\u0192\t\u0192\4\u0193"+
		"\t\u0193\4\u0194\t\u0194\4\u0195\t\u0195\4\u0196\t\u0196\4\u0197\t\u0197"+
		"\4\u0198\t\u0198\4\u0199\t\u0199\4\u019a\t\u019a\4\u019b\t\u019b\4\u019c"+
		"\t\u019c\4\u019d\t\u019d\4\u019e\t\u019e\4\u019f\t\u019f\4\u01a0\t\u01a0"+
		"\4\u01a1\t\u01a1\4\u01a2\t\u01a2\4\u01a3\t\u01a3\4\u01a4\t\u01a4\4\u01a5"+
		"\t\u01a5\4\u01a6\t\u01a6\4\u01a7\t\u01a7\4\u01a8\t\u01a8\4\u01a9\t\u01a9"+
		"\4\u01aa\t\u01aa\4\u01ab\t\u01ab\4\u01ac\t\u01ac\4\u01ad\t\u01ad\4\u01ae"+
		"\t\u01ae\4\u01af\t\u01af\4\u01b0\t\u01b0\4\u01b1\t\u01b1\4\u01b2\t\u01b2"+
		"\4\u01b3\t\u01b3\4\u01b4\t\u01b4\4\u01b5\t\u01b5\4\u01b6\t\u01b6\4\u01b7"+
		"\t\u01b7\4\u01b8\t\u01b8\4\u01b9\t\u01b9\4\u01ba\t\u01ba\4\u01bb\t\u01bb"+
		"\4\u01bc\t\u01bc\4\u01bd\t\u01bd\4\u01be\t\u01be\4\u01bf\t\u01bf\4\u01c0"+
		"\t\u01c0\4\u01c1\t\u01c1\4\u01c2\t\u01c2\4\u01c3\t\u01c3\4\u01c4\t\u01c4"+
		"\4\u01c5\t\u01c5\4\u01c6\t\u01c6\4\u01c7\t\u01c7\4\u01c8\t\u01c8\4\u01c9"+
		"\t\u01c9\4\u01ca\t\u01ca\4\u01cb\t\u01cb\4\u01cc\t\u01cc\4\u01cd\t\u01cd"+
		"\3\2\3\2\5\2\u039d\n\2\3\2\5\2\u03a0\n\2\3\2\5\2\u03a3\n\2\3\2\5\2\u03a6"+
		"\n\2\3\2\5\2\u03a9\n\2\3\2\5\2\u03ac\n\2\3\2\5\2\u03af\n\2\3\2\6\2\u03b2"+
		"\n\2\r\2\16\2\u03b3\3\2\5\2\u03b7\n\2\3\2\5\2\u03ba\n\2\3\2\5\2\u03bd"+
		"\n\2\3\2\5\2\u03c0\n\2\3\2\5\2\u03c3\n\2\3\2\5\2\u03c6\n\2\3\2\5\2\u03c9"+
		"\n\2\3\2\5\2\u03cc\n\2\3\2\5\2\u03cf\n\2\3\2\5\2\u03d2\n\2\3\2\5\2\u03d5"+
		"\n\2\3\2\5\2\u03d8\n\2\3\2\5\2\u03db\n\2\3\2\5\2\u03de\n\2\3\2\5\2\u03e1"+
		"\n\2\3\2\5\2\u03e4\n\2\3\2\5\2\u03e7\n\2\3\2\5\2\u03ea\n\2\3\2\5\2\u03ed"+
		"\n\2\3\2\5\2\u03f0\n\2\3\2\5\2\u03f3\n\2\3\2\5\2\u03f6\n\2\3\2\5\2\u03f9"+
		"\n\2\3\2\5\2\u03fc\n\2\3\2\5\2\u03ff\n\2\3\2\5\2\u0402\n\2\3\2\5\2\u0405"+
		"\n\2\3\2\5\2\u0408\n\2\3\2\5\2\u040b\n\2\3\2\5\2\u040e\n\2\3\2\5\2\u0411"+
		"\n\2\3\2\5\2\u0414\n\2\3\2\5\2\u0417\n\2\3\2\5\2\u041a\n\2\3\2\5\2\u041d"+
		"\n\2\3\2\5\2\u0420\n\2\3\2\5\2\u0423\n\2\3\2\5\2\u0426\n\2\3\2\5\2\u0429"+
		"\n\2\3\2\5\2\u042c\n\2\3\2\5\2\u042f\n\2\3\2\5\2\u0432\n\2\3\2\5\2\u0435"+
		"\n\2\3\2\5\2\u0438\n\2\3\2\5\2\u043b\n\2\3\2\5\2\u043e\n\2\3\2\5\2\u0441"+
		"\n\2\3\2\5\2\u0444\n\2\3\2\5\2\u0447\n\2\3\2\5\2\u044a\n\2\3\2\5\2\u044d"+
		"\n\2\3\2\5\2\u0450\n\2\3\2\5\2\u0453\n\2\3\2\5\2\u0456\n\2\3\2\5\2\u0459"+
		"\n\2\3\2\5\2\u045c\n\2\3\2\5\2\u045f\n\2\3\2\5\2\u0462\n\2\3\2\5\2\u0465"+
		"\n\2\3\2\5\2\u0468\n\2\3\2\5\2\u046b\n\2\3\2\5\2\u046e\n\2\3\2\5\2\u0471"+
		"\n\2\3\2\5\2\u0474\n\2\3\2\5\2\u0477\n\2\3\2\5\2\u047a\n\2\3\2\5\2\u047d"+
		"\n\2\3\2\5\2\u0480\n\2\3\2\5\2\u0483\n\2\3\2\5\2\u0486\n\2\3\2\5\2\u0489"+
		"\n\2\3\2\5\2\u048c\n\2\3\2\5\2\u048f\n\2\3\2\5\2\u0492\n\2\3\2\5\2\u0495"+
		"\n\2\3\2\5\2\u0498\n\2\3\2\5\2\u049b\n\2\3\2\5\2\u049e\n\2\3\2\5\2\u04a1"+
		"\n\2\3\2\5\2\u04a4\n\2\3\2\5\2\u04a7\n\2\3\2\5\2\u04aa\n\2\3\2\5\2\u04ad"+
		"\n\2\3\2\5\2\u04b0\n\2\3\2\3\2\5\2\u04b4\n\2\3\2\5\2\u04b7\n\2\3\2\5\2"+
		"\u04ba\n\2\3\2\5\2\u04bd\n\2\3\2\5\2\u04c0\n\2\3\2\5\2\u04c3\n\2\3\2\3"+
		"\2\3\2\5\2\u04c8\n\2\3\2\5\2\u04cb\n\2\3\2\5\2\u04ce\n\2\3\2\5\2\u04d1"+
		"\n\2\3\2\5\2\u04d4\n\2\3\2\5\2\u04d7\n\2\3\2\5\2\u04da\n\2\3\2\5\2\u04dd"+
		"\n\2\3\2\5\2\u04e0\n\2\3\2\5\2\u04e3\n\2\3\2\5\2\u04e6\n\2\3\2\5\2\u04e9"+
		"\n\2\3\2\5\2\u04ec\n\2\3\2\5\2\u04ef\n\2\3\2\5\2\u04f2\n\2\3\2\5\2\u04f5"+
		"\n\2\3\2\5\2\u04f8\n\2\3\2\5\2\u04fb\n\2\3\2\5\2\u04fe\n\2\3\2\5\2\u0501"+
		"\n\2\3\2\5\2\u0504\n\2\3\2\5\2\u0507\n\2\3\2\5\2\u050a\n\2\3\2\5\2\u050d"+
		"\n\2\3\2\5\2\u0510\n\2\3\2\5\2\u0513\n\2\3\2\5\2\u0516\n\2\3\2\5\2\u0519"+
		"\n\2\3\2\5\2\u051c\n\2\3\2\5\2\u051f\n\2\3\2\5\2\u0522\n\2\3\2\5\2\u0525"+
		"\n\2\3\2\5\2\u0528\n\2\3\2\5\2\u052b\n\2\3\2\5\2\u052e\n\2\3\2\5\2\u0531"+
		"\n\2\3\2\5\2\u0534\n\2\3\2\5\2\u0537\n\2\3\2\5\2\u053a\n\2\3\2\5\2\u053d"+
		"\n\2\3\2\5\2\u0540\n\2\3\2\5\2\u0543\n\2\3\2\5\2\u0546\n\2\3\2\5\2\u0549"+
		"\n\2\3\2\5\2\u054c\n\2\3\2\5\2\u054f\n\2\3\2\5\2\u0552\n\2\3\2\5\2\u0555"+
		"\n\2\3\2\5\2\u0558\n\2\3\2\5\2\u055b\n\2\3\2\5\2\u055e\n\2\3\2\5\2\u0561"+
		"\n\2\3\2\5\2\u0564\n\2\3\2\5\2\u0567\n\2\3\2\5\2\u056a\n\2\3\2\5\2\u056d"+
		"\n\2\3\2\5\2\u0570\n\2\3\2\5\2\u0573\n\2\3\2\5\2\u0576\n\2\3\2\5\2\u0579"+
		"\n\2\3\2\5\2\u057c\n\2\3\2\5\2\u057f\n\2\3\2\5\2\u0582\n\2\3\2\5\2\u0585"+
		"\n\2\3\2\5\2\u0588\n\2\3\2\5\2\u058b\n\2\3\2\5\2\u058e\n\2\3\2\5\2\u0591"+
		"\n\2\3\2\5\2\u0594\n\2\3\2\5\2\u0597\n\2\3\2\5\2\u059a\n\2\3\2\5\2\u059d"+
		"\n\2\3\2\5\2\u05a0\n\2\3\2\5\2\u05a3\n\2\3\2\5\2\u05a6\n\2\3\2\5\2\u05a9"+
		"\n\2\3\2\5\2\u05ac\n\2\3\2\5\2\u05af\n\2\3\2\5\2\u05b2\n\2\3\2\5\2\u05b5"+
		"\n\2\3\2\5\2\u05b8\n\2\3\2\5\2\u05bb\n\2\3\2\5\2\u05be\n\2\3\2\5\2\u05c1"+
		"\n\2\3\2\5\2\u05c4\n\2\3\2\3\2\5\2\u05c8\n\2\3\2\5\2\u05cb\n\2\3\2\3\2"+
		"\3\2\3\2\5\2\u05d1\n\2\3\2\5\2\u05d4\n\2\3\2\6\2\u05d7\n\2\r\2\16\2\u05d8"+
		"\3\2\3\2\3\2\5\2\u05de\n\2\3\2\5\2\u05e1\n\2\3\2\5\2\u05e4\n\2\3\2\5\2"+
		"\u05e7\n\2\3\2\5\2\u05ea\n\2\3\2\5\2\u05ed\n\2\3\2\5\2\u05f0\n\2\3\2\5"+
		"\2\u05f3\n\2\3\2\5\2\u05f6\n\2\3\2\5\2\u05f9\n\2\3\2\5\2\u05fc\n\2\3\2"+
		"\5\2\u05ff\n\2\3\2\5\2\u0602\n\2\3\2\5\2\u0605\n\2\3\2\5\2\u0608\n\2\3"+
		"\2\5\2\u060b\n\2\3\2\5\2\u060e\n\2\3\2\5\2\u0611\n\2\3\2\5\2\u0614\n\2"+
		"\3\2\3\2\5\2\u0618\n\2\3\2\5\2\u061b\n\2\3\2\5\2\u061e\n\2\3\2\5\2\u0621"+
		"\n\2\3\2\5\2\u0624\n\2\3\2\5\2\u0627\n\2\3\2\5\2\u062a\n\2\3\2\5\2\u062d"+
		"\n\2\3\2\5\2\u0630\n\2\3\2\5\2\u0633\n\2\3\2\5\2\u0636\n\2\3\2\5\2\u0639"+
		"\n\2\3\2\5\2\u063c\n\2\3\2\5\2\u063f\n\2\3\2\5\2\u0642\n\2\3\2\5\2\u0645"+
		"\n\2\3\2\5\2\u0648\n\2\3\2\5\2\u064b\n\2\3\2\5\2\u064e\n\2\3\2\5\2\u0651"+
		"\n\2\3\2\5\2\u0654\n\2\3\2\5\2\u0657\n\2\3\2\5\2\u065a\n\2\3\2\5\2\u065d"+
		"\n\2\3\2\5\2\u0660\n\2\3\2\5\2\u0663\n\2\3\2\5\2\u0666\n\2\3\2\5\2\u0669"+
		"\n\2\3\2\5\2\u066c\n\2\3\2\5\2\u066f\n\2\3\2\5\2\u0672\n\2\3\2\5\2\u0675"+
		"\n\2\3\2\5\2\u0678\n\2\3\2\5\2\u067b\n\2\3\2\5\2\u067e\n\2\3\2\5\2\u0681"+
		"\n\2\3\2\5\2\u0684\n\2\3\2\5\2\u0687\n\2\3\2\5\2\u068a\n\2\3\2\5\2\u068d"+
		"\n\2\3\2\5\2\u0690\n\2\3\2\3\2\5\2\u0694\n\2\3\2\5\2\u0697\n\2\3\2\5\2"+
		"\u069a\n\2\3\2\5\2\u069d\n\2\3\2\5\2\u06a0\n\2\3\2\5\2\u06a3\n\2\3\2\5"+
		"\2\u06a6\n\2\3\2\5\2\u06a9\n\2\3\2\5\2\u06ac\n\2\3\2\5\2\u06af\n\2\3\2"+
		"\5\2\u06b2\n\2\3\2\5\2\u06b5\n\2\3\2\5\2\u06b8\n\2\3\2\5\2\u06bb\n\2\3"+
		"\2\5\2\u06be\n\2\3\2\5\2\u06c1\n\2\3\2\5\2\u06c4\n\2\3\2\5\2\u06c7\n\2"+
		"\3\2\5\2\u06ca\n\2\3\2\5\2\u06cd\n\2\3\2\5\2\u06d0\n\2\3\2\5\2\u06d3\n"+
		"\2\3\2\5\2\u06d6\n\2\3\2\5\2\u06d9\n\2\3\2\5\2\u06dc\n\2\3\2\5\2\u06df"+
		"\n\2\3\2\5\2\u06e2\n\2\3\2\5\2\u06e5\n\2\3\2\5\2\u06e8\n\2\3\2\5\2\u06eb"+
		"\n\2\3\2\5\2\u06ee\n\2\3\2\5\2\u06f1\n\2\3\2\5\2\u06f4\n\2\3\2\5\2\u06f7"+
		"\n\2\3\2\5\2\u06fa\n\2\3\2\5\2\u06fd\n\2\3\2\5\2\u0700\n\2\3\2\5\2\u0703"+
		"\n\2\3\2\5\2\u0706\n\2\3\2\5\2\u0709\n\2\3\2\5\2\u070c\n\2\3\2\3\2\5\2"+
		"\u0710\n\2\3\2\5\2\u0713\n\2\3\2\5\2\u0716\n\2\3\2\5\2\u0719\n\2\3\2\5"+
		"\2\u071c\n\2\3\2\5\2\u071f\n\2\3\2\3\2\3\2\3\2\5\2\u0725\n\2\3\2\5\2\u0728"+
		"\n\2\3\2\5\2\u072b\n\2\3\2\5\2\u072e\n\2\3\2\5\2\u0731\n\2\3\2\5\2\u0734"+
		"\n\2\3\2\6\2\u0737\n\2\r\2\16\2\u0738\3\2\3\2\3\2\5\2\u073e\n\2\3\2\5"+
		"\2\u0741\n\2\3\2\5\2\u0744\n\2\3\2\5\2\u0747\n\2\3\2\5\2\u074a\n\2\3\2"+
		"\5\2\u074d\n\2\3\2\5\2\u0750\n\2\3\2\5\2\u0753\n\2\3\2\5\2\u0756\n\2\3"+
		"\2\5\2\u0759\n\2\3\2\5\2\u075c\n\2\3\2\5\2\u075f\n\2\3\2\5\2\u0762\n\2"+
		"\3\2\5\2\u0765\n\2\3\2\5\2\u0768\n\2\3\2\5\2\u076b\n\2\3\2\5\2\u076e\n"+
		"\2\3\2\5\2\u0771\n\2\3\2\5\2\u0774\n\2\3\2\5\2\u0777\n\2\3\2\5\2\u077a"+
		"\n\2\3\2\5\2\u077d\n\2\3\2\5\2\u0780\n\2\3\2\5\2\u0783\n\2\3\2\5\2\u0786"+
		"\n\2\3\2\5\2\u0789\n\2\3\2\5\2\u078c\n\2\3\2\5\2\u078f\n\2\3\2\5\2\u0792"+
		"\n\2\3\2\5\2\u0795\n\2\3\2\5\2\u0798\n\2\3\2\5\2\u079b\n\2\3\2\5\2\u079e"+
		"\n\2\3\2\5\2\u07a1\n\2\3\2\5\2\u07a4\n\2\3\2\5\2\u07a7\n\2\3\2\5\2\u07aa"+
		"\n\2\3\2\5\2\u07ad\n\2\3\2\5\2\u07b0\n\2\3\2\3\2\3\2\5\2\u07b5\n\2\3\2"+
		"\5\2\u07b8\n\2\3\2\5\2\u07bb\n\2\3\2\5\2\u07be\n\2\3\2\5\2\u07c1\n\2\3"+
		"\2\5\2\u07c4\n\2\3\2\5\2\u07c7\n\2\3\2\5\2\u07ca\n\2\3\2\5\2\u07cd\n\2"+
		"\3\2\5\2\u07d0\n\2\3\2\5\2\u07d3\n\2\3\2\5\2\u07d6\n\2\3\2\5\2\u07d9\n"+
		"\2\3\2\5\2\u07dc\n\2\3\2\5\2\u07df\n\2\3\2\5\2\u07e2\n\2\3\2\5\2\u07e5"+
		"\n\2\3\2\5\2\u07e8\n\2\3\2\5\2\u07eb\n\2\3\2\5\2\u07ee\n\2\3\2\5\2\u07f1"+
		"\n\2\3\2\5\2\u07f4\n\2\3\2\5\2\u07f7\n\2\3\2\5\2\u07fa\n\2\3\2\5\2\u07fd"+
		"\n\2\3\2\5\2\u0800\n\2\3\2\5\2\u0803\n\2\3\2\5\2\u0806\n\2\3\2\5\2\u0809"+
		"\n\2\3\2\5\2\u080c\n\2\3\2\5\2\u080f\n\2\3\2\5\2\u0812\n\2\3\2\5\2\u0815"+
		"\n\2\3\2\5\2\u0818\n\2\3\2\3\2\3\2\3\2\3\2\5\2\u081f\n\2\3\2\5\2\u0822"+
		"\n\2\3\2\5\2\u0825\n\2\3\2\5\2\u0828\n\2\3\2\5\2\u082b\n\2\3\2\5\2\u082e"+
		"\n\2\3\2\5\2\u0831\n\2\3\2\5\2\u0834\n\2\3\2\5\2\u0837\n\2\3\2\5\2\u083a"+
		"\n\2\3\2\5\2\u083d\n\2\3\2\5\2\u0840\n\2\3\2\5\2\u0843\n\2\3\2\5\2\u0846"+
		"\n\2\3\2\5\2\u0849\n\2\3\2\5\2\u084c\n\2\3\2\5\2\u084f\n\2\3\2\5\2\u0852"+
		"\n\2\3\2\5\2\u0855\n\2\3\2\5\2\u0858\n\2\3\2\5\2\u085b\n\2\3\2\5\2\u085e"+
		"\n\2\3\2\5\2\u0861\n\2\3\2\5\2\u0864\n\2\3\2\5\2\u0867\n\2\3\2\5\2\u086a"+
		"\n\2\3\2\5\2\u086d\n\2\3\2\5\2\u0870\n\2\3\2\5\2\u0873\n\2\3\2\5\2\u0876"+
		"\n\2\3\2\3\2\3\2\3\2\3\2\5\2\u087d\n\2\3\2\5\2\u0880\n\2\3\2\5\2\u0883"+
		"\n\2\3\2\5\2\u0886\n\2\3\2\5\2\u0889\n\2\3\2\5\2\u088c\n\2\3\2\5\2\u088f"+
		"\n\2\3\2\5\2\u0892\n\2\3\2\5\2\u0895\n\2\3\2\5\2\u0898\n\2\3\2\5\2\u089b"+
		"\n\2\3\2\5\2\u089e\n\2\3\2\5\2\u08a1\n\2\3\2\5\2\u08a4\n\2\3\2\5\2\u08a7"+
		"\n\2\3\2\5\2\u08aa\n\2\3\2\5\2\u08ad\n\2\3\2\5\2\u08b0\n\2\3\2\5\2\u08b3"+
		"\n\2\3\2\5\2\u08b6\n\2\3\2\5\2\u08b9\n\2\3\2\5\2\u08bc\n\2\3\2\5\2\u08bf"+
		"\n\2\3\2\5\2\u08c2\n\2\3\2\5\2\u08c5\n\2\3\2\3\2\3\2\5\2\u08ca\n\2\3\2"+
		"\5\2\u08cd\n\2\3\2\5\2\u08d0\n\2\3\2\5\2\u08d3\n\2\3\2\5\2\u08d6\n\2\3"+
		"\2\5\2\u08d9\n\2\3\2\5\2\u08dc\n\2\3\2\5\2\u08df\n\2\3\2\5\2\u08e2\n\2"+
		"\3\2\5\2\u08e5\n\2\3\2\5\2\u08e8\n\2\3\2\5\2\u08eb\n\2\3\2\5\2\u08ee\n"+
		"\2\3\2\5\2\u08f1\n\2\3\2\5\2\u08f4\n\2\3\2\5\2\u08f7\n\2\3\2\5\2\u08fa"+
		"\n\2\3\2\5\2\u08fd\n\2\3\2\5\2\u0900\n\2\3\2\3\2\3\2\5\2\u0905\n\2\3\2"+
		"\5\2\u0908\n\2\3\2\5\2\u090b\n\2\3\2\5\2\u090e\n\2\3\2\5\2\u0911\n\2\3"+
		"\2\5\2\u0914\n\2\3\2\5\2\u0917\n\2\3\2\5\2\u091a\n\2\3\2\5\2\u091d\n\2"+
		"\3\2\5\2\u0920\n\2\3\2\5\2\u0923\n\2\3\2\5\2\u0926\n\2\3\2\5\2\u0929\n"+
		"\2\3\2\5\2\u092c\n\2\3\2\5\2\u092f\n\2\3\2\5\2\u0932\n\2\3\2\5\2\u0935"+
		"\n\2\3\2\5\2\u0938\n\2\3\2\5\2\u093b\n\2\3\2\5\2\u093e\n\2\3\2\5\2\u0941"+
		"\n\2\3\2\5\2\u0944\n\2\3\2\5\2\u0947\n\2\3\2\5\2\u094a\n\2\3\2\5\2\u094d"+
		"\n\2\3\2\5\2\u0950\n\2\3\2\5\2\u0953\n\2\3\2\5\2\u0956\n\2\3\2\5\2\u0959"+
		"\n\2\3\2\3\2\5\2\u095d\n\2\3\2\5\2\u0960\n\2\3\2\5\2\u0963\n\2\3\2\5\2"+
		"\u0966\n\2\3\2\5\2\u0969\n\2\3\2\5\2\u096c\n\2\3\2\5\2\u096f\n\2\3\2\5"+
		"\2\u0972\n\2\3\2\5\2\u0975\n\2\3\2\5\2\u0978\n\2\3\2\5\2\u097b\n\2\3\2"+
		"\5\2\u097e\n\2\3\2\3\2\5\2\u0982\n\2\3\2\5\2\u0985\n\2\3\2\5\2\u0988\n"+
		"\2\3\2\5\2\u098b\n\2\3\2\3\2\5\2\u098f\n\2\3\2\3\2\5\2\u0993\n\2\3\2\5"+
		"\2\u0996\n\2\3\2\5\2\u0999\n\2\3\2\5\2\u099c\n\2\3\2\5\2\u099f\n\2\3\2"+
		"\5\2\u09a2\n\2\3\2\5\2\u09a5\n\2\3\2\5\2\u09a8\n\2\3\2\3\2\5\2\u09ac\n"+
		"\2\3\2\5\2\u09af\n\2\3\2\5\2\u09b2\n\2\3\2\5\2\u09b5\n\2\3\2\3\2\5\2\u09b9"+
		"\n\2\3\2\5\2\u09bc\n\2\3\2\5\2\u09bf\n\2\3\2\5\2\u09c2\n\2\3\2\5\2\u09c5"+
		"\n\2\3\2\5\2\u09c8\n\2\3\2\5\2\u09cb\n\2\3\2\5\2\u09ce\n\2\3\2\6\2\u09d1"+
		"\n\2\r\2\16\2\u09d2\3\2\3\2\5\2\u09d7\n\2\3\2\5\2\u09da\n\2\3\2\3\2\5"+
		"\2\u09de\n\2\3\2\5\2\u09e1\n\2\3\2\5\2\u09e4\n\2\3\2\5\2\u09e7\n\2\3\2"+
		"\5\2\u09ea\n\2\3\2\3\2\5\2\u09ee\n\2\3\2\5\2\u09f1\n\2\3\2\5\2\u09f4\n"+
		"\2\3\2\3\2\6\2\u09f8\n\2\r\2\16\2\u09f9\3\2\3\2\5\2\u09fe\n\2\3\2\5\2"+
		"\u0a01\n\2\3\2\5\2\u0a04\n\2\3\2\5\2\u0a07\n\2\3\2\3\2\6\2\u0a0b\n\2\r"+
		"\2\16\2\u0a0c\3\2\3\2\5\2\u0a11\n\2\3\2\5\2\u0a14\n\2\3\2\5\2\u0a17\n"+
		"\2\3\2\5\2\u0a1a\n\2\3\2\5\2\u0a1d\n\2\3\2\6\2\u0a20\n\2\r\2\16\2\u0a21"+
		"\3\2\3\2\5\2\u0a26\n\2\3\2\5\2\u0a29\n\2\3\2\5\2\u0a2c\n\2\3\2\5\2\u0a2f"+
		"\n\2\3\2\5\2\u0a32\n\2\3\2\6\2\u0a35\n\2\r\2\16\2\u0a36\3\2\3\2\5\2\u0a3b"+
		"\n\2\3\2\5\2\u0a3e\n\2\3\2\5\2\u0a41\n\2\3\2\5\2\u0a44\n\2\3\2\5\2\u0a47"+
		"\n\2\3\2\6\2\u0a4a\n\2\r\2\16\2\u0a4b\3\2\3\2\5\2\u0a50\n\2\3\2\5\2\u0a53"+
		"\n\2\3\2\5\2\u0a56\n\2\3\2\5\2\u0a59\n\2\3\2\3\2\6\2\u0a5d\n\2\r\2\16"+
		"\2\u0a5e\3\2\3\2\5\2\u0a63\n\2\3\2\5\2\u0a66\n\2\3\2\3\2\5\2\u0a6a\n\2"+
		"\3\2\5\2\u0a6d\n\2\3\2\5\2\u0a70\n\2\3\2\5\2\u0a73\n\2\3\2\3\2\5\2\u0a77"+
		"\n\2\3\2\5\2\u0a7a\n\2\3\2\5\2\u0a7d\n\2\3\2\5\2\u0a80\n\2\3\2\5\2\u0a83"+
		"\n\2\3\2\3\2\3\2\3\2\3\2\5\2\u0a8a\n\2\3\2\5\2\u0a8d\n\2\3\2\5\2\u0a90"+
		"\n\2\3\2\5\2\u0a93\n\2\3\2\5\2\u0a96\n\2\3\2\5\2\u0a99\n\2\3\2\5\2\u0a9c"+
		"\n\2\3\2\5\2\u0a9f\n\2\3\2\3\2\5\2\u0aa3\n\2\3\2\5\2\u0aa6\n\2\3\2\5\2"+
		"\u0aa9\n\2\3\2\5\2\u0aac\n\2\3\2\5\2\u0aaf\n\2\3\2\5\2\u0ab2\n\2\3\2\5"+
		"\2\u0ab5\n\2\3\2\5\2\u0ab8\n\2\3\2\5\2\u0abb\n\2\3\2\5\2\u0abe\n\2\3\2"+
		"\5\2\u0ac1\n\2\3\2\5\2\u0ac4\n\2\3\2\5\2\u0ac7\n\2\3\2\5\2\u0aca\n\2\3"+
		"\2\5\2\u0acd\n\2\3\2\5\2\u0ad0\n\2\3\2\5\2\u0ad3\n\2\3\2\5\2\u0ad6\n\2"+
		"\3\2\5\2\u0ad9\n\2\3\2\5\2\u0adc\n\2\3\2\5\2\u0adf\n\2\3\2\5\2\u0ae2\n"+
		"\2\3\2\5\2\u0ae5\n\2\3\2\5\2\u0ae8\n\2\3\2\5\2\u0aeb\n\2\3\2\5\2\u0aee"+
		"\n\2\3\2\5\2\u0af1\n\2\3\2\5\2\u0af4\n\2\3\2\5\2\u0af7\n\2\3\2\5\2\u0afa"+
		"\n\2\3\2\5\2\u0afd\n\2\3\2\5\2\u0b00\n\2\3\2\5\2\u0b03\n\2\3\2\5\2\u0b06"+
		"\n\2\3\2\5\2\u0b09\n\2\3\2\5\2\u0b0c\n\2\3\2\5\2\u0b0f\n\2\3\2\5\2\u0b12"+
		"\n\2\3\2\5\2\u0b15\n\2\3\2\5\2\u0b18\n\2\3\2\3\2\5\2\u0b1c\n\2\3\2\5\2"+
		"\u0b1f\n\2\3\2\5\2\u0b22\n\2\3\2\5\2\u0b25\n\2\3\2\5\2\u0b28\n\2\3\2\5"+
		"\2\u0b2b\n\2\3\2\5\2\u0b2e\n\2\3\2\5\2\u0b31\n\2\3\2\5\2\u0b34\n\2\3\2"+
		"\5\2\u0b37\n\2\3\2\5\2\u0b3a\n\2\3\2\5\2\u0b3d\n\2\3\2\5\2\u0b40\n\2\3"+
		"\2\5\2\u0b43\n\2\3\2\5\2\u0b46\n\2\3\2\5\2\u0b49\n\2\3\2\5\2\u0b4c\n\2"+
		"\3\2\5\2\u0b4f\n\2\3\2\5\2\u0b52\n\2\3\2\5\2\u0b55\n\2\3\2\5\2\u0b58\n"+
		"\2\3\2\5\2\u0b5b\n\2\3\2\5\2\u0b5e\n\2\3\2\5\2\u0b61\n\2\3\2\3\2\5\2\u0b65"+
		"\n\2\3\2\5\2\u0b68\n\2\3\2\5\2\u0b6b\n\2\3\2\3\2\5\2\u0b6f\n\2\3\2\5\2"+
		"\u0b72\n\2\3\2\5\2\u0b75\n\2\3\2\5\2\u0b78\n\2\3\2\5\2\u0b7b\n\2\3\2\5"+
		"\2\u0b7e\n\2\3\2\5\2\u0b81\n\2\3\2\3\2\5\2\u0b85\n\2\3\2\5\2\u0b88\n\2"+
		"\3\2\3\2\5\2\u0b8c\n\2\3\2\6\2\u0b8f\n\2\r\2\16\2\u0b90\3\2\3\2\5\2\u0b95"+
		"\n\2\3\2\5\2\u0b98\n\2\3\2\5\2\u0b9b\n\2\3\2\5\2\u0b9e\n\2\3\2\3\2\3\2"+
		"\3\2\5\2\u0ba4\n\2\3\2\5\2\u0ba7\n\2\5\2\u0ba9\n\2\3\3\3\3\3\3\3\4\3\4"+
		"\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3\r"+
		"\3\r\3\r\3\16\3\16\3\16\3\17\3\17\3\17\5\17\u0bc9\n\17\3\20\3\20\3\20"+
		"\3\21\3\21\3\22\3\22\3\23\3\23\3\23\3\24\3\24\3\25\3\25\3\26\3\26\3\27"+
		"\3\27\3\30\3\30\3\31\3\31\3\32\3\32\3\33\3\33\3\34\3\34\3\34\3\35\3\35"+
		"\3\36\3\36\3\36\3\37\3\37\3\37\3 \3 \3!\3!\3\"\3\"\3\"\3#\3#\3$\3$\3$"+
		"\3%\3%\3&\3&\3\'\3\'\3(\3(\3)\3)\3*\6*\u0c07\n*\r*\16*\u0c08\3+\3+\3,"+
		"\3,\3,\3-\3-\3-\3.\3.\3.\3.\3/\3/\3\60\3\60\3\61\3\61\3\61\3\62\3\62\3"+
		"\63\3\63\3\63\3\64\3\64\3\65\3\65\3\66\3\66\3\67\3\67\3\67\5\67\u0c2c"+
		"\n\67\3\67\3\67\38\38\39\39\39\3:\3:\3:\3;\6;\u0c39\n;\r;\16;\u0c3a\3"+
		"<\3<\3=\3=\3>\3>\3?\3?\3@\3@\3@\3A\3A\3B\3B\3C\3C\3D\3D\3E\3E\3F\3F\3"+
		"F\3G\3G\3H\3H\3I\3I\3J\6J\u0c5c\nJ\rJ\16J\u0c5d\3K\3K\3L\3L\3M\3M\3N\3"+
		"N\3O\3O\3P\3P\7P\u0c6c\nP\fP\16P\u0c6f\13P\3Q\3Q\3Q\5Q\u0c74\nQ\3R\3R"+
		"\3S\3S\5S\u0c7a\nS\3T\3T\3U\3U\3U\3V\3V\3W\3W\3W\3X\3X\3Y\3Y\3Z\3Z\3["+
		"\3[\6[\u0c8e\n[\r[\16[\u0c8f\3\\\3\\\3\\\3\\\3]\3]\3^\3^\3_\3_\3`\3`\3"+
		"a\3a\3b\3b\3c\3c\3c\3d\3d\3e\3e\3e\3f\3f\3f\3g\3g\3h\3h\3i\3i\3i\3j\3"+
		"j\3k\3k\3l\3l\3m\3m\3n\3n\3n\3o\3o\3o\3p\3p\3p\3q\5q\u0cc6\nq\3q\5q\u0cc9"+
		"\nq\3q\5q\u0ccc\nq\5q\u0cce\nq\3r\3r\3s\3s\3t\3t\3u\3u\3v\3v\3v\3w\3w"+
		"\3w\3x\3x\3x\5x\u0ce1\nx\3y\3y\3z\3z\3{\3{\3{\3|\3|\3}\5}\u0ced\n}\3}"+
		"\5}\u0cf0\n}\3}\5}\u0cf3\n}\5}\u0cf5\n}\3~\3~\3\177\3\177\3\u0080\3\u0080"+
		"\3\u0081\3\u0081\3\u0082\3\u0082\3\u0083\3\u0083\3\u0084\3\u0084\3\u0084"+
		"\3\u0085\3\u0085\3\u0086\3\u0086\3\u0087\3\u0087\3\u0088\3\u0088\3\u0088"+
		"\3\u0089\3\u0089\3\u008a\3\u008a\3\u008b\3\u008b\3\u008c\3\u008c\3\u008c"+
		"\3\u008d\3\u008d\3\u008e\3\u008e\3\u008f\3\u008f\3\u0090\3\u0090\3\u0091"+
		"\3\u0091\3\u0092\3\u0092\3\u0093\3\u0093\3\u0094\3\u0094\3\u0095\3\u0095"+
		"\3\u0096\6\u0096\u0d2b\n\u0096\r\u0096\16\u0096\u0d2c\3\u0097\3\u0097"+
		"\3\u0098\3\u0098\3\u0099\3\u0099\3\u009a\3\u009a\3\u009a\3\u009b\3\u009b"+
		"\3\u009c\3\u009c\3\u009d\3\u009d\3\u009e\3\u009e\3\u009f\3\u009f\3\u009f"+
		"\3\u00a0\3\u00a0\3\u00a1\3\u00a1\3\u00a2\3\u00a2\3\u00a2\3\u00a2\3\u00a3"+
		"\3\u00a3\3\u00a4\3\u00a4\3\u00a4\3\u00a5\3\u00a5\3\u00a6\3\u00a6\3\u00a7"+
		"\6\u00a7\u0d55\n\u00a7\r\u00a7\16\u00a7\u0d56\3\u00a8\3\u00a8\3\u00a9"+
		"\3\u00a9\3\u00a9\3\u00aa\3\u00aa\3\u00ab\5\u00ab\u0d61\n\u00ab\3\u00ab"+
		"\5\u00ab\u0d64\n\u00ab\3\u00ab\5\u00ab\u0d67\n\u00ab\5\u00ab\u0d69\n\u00ab"+
		"\3\u00ac\3\u00ac\3\u00ad\3\u00ad\3\u00ae\3\u00ae\3\u00ae\3\u00af\3\u00af"+
		"\3\u00b0\3\u00b0\3\u00b1\6\u00b1\u0d77\n\u00b1\r\u00b1\16\u00b1\u0d78"+
		"\3\u00b2\3\u00b2\3\u00b3\3\u00b3\3\u00b3\3\u00b4\3\u00b4\3\u00b5\3\u00b5"+
		"\3\u00b6\3\u00b6\3\u00b7\3\u00b7\3\u00b7\3\u00b8\3\u00b8\3\u00b9\3\u00b9"+
		"\3\u00ba\6\u00ba\u0d8e\n\u00ba\r\u00ba\16\u00ba\u0d8f\3\u00bb\3\u00bb"+
		"\3\u00bc\3\u00bc\3\u00bd\3\u00bd\3\u00be\6\u00be\u0d99\n\u00be\r\u00be"+
		"\16\u00be\u0d9a\3\u00bf\3\u00bf\3\u00c0\3\u00c0\5\u00c0\u0da1\n\u00c0"+
		"\3\u00c1\3\u00c1\3\u00c1\3\u00c1\3\u00c1\3\u00c1\3\u00c1\3\u00c2\3\u00c2"+
		"\3\u00c3\6\u00c3\u0dad\n\u00c3\r\u00c3\16\u00c3\u0dae\3\u00c4\3\u00c4"+
		"\3\u00c4\3\u00c5\3\u00c5\3\u00c5\3\u00c6\3\u00c6\3\u00c6\3\u00c7\3\u00c7"+
		"\3\u00c7\3\u00c8\3\u00c8\3\u00c8\3\u00c9\3\u00c9\3\u00ca\3\u00ca\3\u00cb"+
		"\6\u00cb\u0dc5\n\u00cb\r\u00cb\16\u00cb\u0dc6\3\u00cc\3\u00cc\3\u00cc"+
		"\3\u00cd\3\u00cd\3\u00ce\3\u00ce\3\u00ce\3\u00cf\3\u00cf\3\u00d0\3\u00d0"+
		"\3\u00d0\3\u00d1\3\u00d1\3\u00d2\3\u00d2\3\u00d3\3\u00d3\3\u00d4\3\u00d4"+
		"\3\u00d4\3\u00d5\3\u00d5\3\u00d6\3\u00d6\3\u00d7\3\u00d7\3\u00d8\3\u00d8"+
		"\3\u00d9\3\u00d9\3\u00da\3\u00da\3\u00db\3\u00db\3\u00db\3\u00dc\3\u00dc"+
		"\3\u00dc\3\u00dd\3\u00dd\3\u00de\3\u00de\3\u00df\3\u00df\3\u00e0\5\u00e0"+
		"\u0df8\n\u00e0\3\u00e0\5\u00e0\u0dfb\n\u00e0\5\u00e0\u0dfd\n\u00e0\3\u00e1"+
		"\3\u00e1\3\u00e1\3\u00e2\3\u00e2\3\u00e3\3\u00e3\3\u00e4\3\u00e4\3\u00e4"+
		"\3\u00e5\3\u00e5\3\u00e6\3\u00e6\3\u00e7\3\u00e7\3\u00e8\3\u00e8\3\u00e9"+
		"\3\u00e9\3\u00ea\3\u00ea\3\u00ea\3\u00eb\3\u00eb\3\u00ec\3\u00ec\3\u00ec"+
		"\3\u00ed\3\u00ed\3\u00ed\3\u00ee\3\u00ee\3\u00ef\3\u00ef\3\u00ef\3\u00f0"+
		"\3\u00f0\3\u00f1\3\u00f1\3\u00f2\3\u00f2\3\u00f3\3\u00f3\3\u00f4\3\u00f4"+
		"\3\u00f4\3\u00f5\3\u00f5\3\u00f5\3\u00f6\3\u00f6\3\u00f6\3\u00f7\3\u00f7"+
		"\3\u00f8\3\u00f8\5\u00f8\u0e38\n\u00f8\3\u00f9\3\u00f9\3\u00f9\3\u00fa"+
		"\3\u00fa\3\u00fb\3\u00fb\3\u00fb\3\u00fc\3\u00fc\3\u00fc\3\u00fd\3\u00fd"+
		"\3\u00fe\6\u00fe\u0e48\n\u00fe\r\u00fe\16\u00fe\u0e49\3\u00ff\3\u00ff"+
		"\3\u0100\3\u0100\3\u0101\3\u0101\3\u0101\3\u0102\6\u0102\u0e54\n\u0102"+
		"\r\u0102\16\u0102\u0e55\3\u0103\3\u0103\3\u0104\3\u0104\3\u0104\3\u0105"+
		"\3\u0105\3\u0106\3\u0106\3\u0106\3\u0107\3\u0107\3\u0108\3\u0108\3\u0108"+
		"\3\u0109\3\u0109\3\u010a\3\u010a\3\u010b\3\u010b\3\u010c\3\u010c\3\u010d"+
		"\3\u010d\3\u010e\3\u010e\3\u010e\3\u010f\3\u010f\3\u0110\3\u0110\3\u0111"+
		"\3\u0111\3\u0111\5\u0111\u0e7b\n\u0111\3\u0111\3\u0111\3\u0112\3\u0112"+
		"\3\u0113\3\u0113\3\u0114\3\u0114\3\u0114\3\u0115\5\u0115\u0e87\n\u0115"+
		"\3\u0115\5\u0115\u0e8a\n\u0115\5\u0115\u0e8c\n\u0115\3\u0116\3\u0116\3"+
		"\u0117\3\u0117\3\u0118\3\u0118\3\u0119\3\u0119\3\u0119\3\u011a\3\u011a"+
		"\3\u011b\3\u011b\3\u011c\3\u011c\3\u011d\3\u011d\3\u011e\3\u011e\3\u011f"+
		"\3\u011f\3\u011f\3\u0120\3\u0120\3\u0121\3\u0121\3\u0122\3\u0122\3\u0123"+
		"\3\u0123\3\u0124\3\u0124\3\u0124\3\u0125\5\u0125\u0eb0\n\u0125\3\u0125"+
		"\5\u0125\u0eb3\n\u0125\5\u0125\u0eb5\n\u0125\3\u0126\3\u0126\3\u0126\5"+
		"\u0126\u0eba\n\u0126\5\u0126\u0ebc\n\u0126\3\u0127\3\u0127\3\u0128\3\u0128"+
		"\3\u0129\3\u0129\3\u012a\3\u012a\3\u012a\3\u012b\3\u012b\3\u012c\3\u012c"+
		"\3\u012c\3\u012d\3\u012d\3\u012e\3\u012e\3\u012f\3\u012f\3\u0130\3\u0130"+
		"\3\u0131\3\u0131\3\u0132\3\u0132\3\u0132\3\u0133\3\u0133\3\u0134\3\u0134"+
		"\3\u0134\3\u0135\3\u0135\3\u0136\3\u0136\3\u0137\3\u0137\3\u0138\3\u0138"+
		"\3\u0139\3\u0139\3\u013a\6\u013a\u0ee9\n\u013a\r\u013a\16\u013a\u0eea"+
		"\3\u013b\3\u013b\3\u013b\3\u013c\3\u013c\3\u013d\3\u013d\3\u013d\3\u013e"+
		"\3\u013e\3\u013f\3\u013f\3\u0140\3\u0140\3\u0141\3\u0141\3\u0141\3\u0141"+
		"\3\u0142\3\u0142\3\u0143\3\u0143\3\u0144\3\u0144\3\u0145\3\u0145\3\u0146"+
		"\3\u0146\3\u0147\3\u0147\3\u0147\3\u0148\3\u0148\3\u0149\3\u0149\3\u014a"+
		"\3\u014a\3\u014b\3\u014b\3\u014b\3\u014b\3\u014c\3\u014c\3\u014d\3\u014d"+
		"\3\u014e\3\u014e\3\u014f\3\u014f\3\u0150\3\u0150\3\u0150\3\u0150\3\u0150"+
		"\3\u0150\3\u0150\3\u0151\6\u0151\u0f26\n\u0151\r\u0151\16\u0151\u0f27"+
		"\3\u0152\3\u0152\3\u0153\3\u0153\3\u0154\3\u0154\3\u0155\3\u0155\7\u0155"+
		"\u0f32\n\u0155\f\u0155\16\u0155\u0f35\13\u0155\3\u0156\3\u0156\3\u0157"+
		"\3\u0157\3\u0157\3\u0158\3\u0158\3\u0159\3\u0159\3\u015a\6\u015a\u0f41"+
		"\n\u015a\r\u015a\16\u015a\u0f42\3\u015b\3\u015b\3\u015b\3\u015c\3\u015c"+
		"\3\u015d\3\u015d\3\u015e\3\u015e\3\u015f\3\u015f\3\u0160\3\u0160\3\u0161"+
		"\3\u0161\3\u0162\3\u0162\3\u0163\3\u0163\3\u0164\3\u0164\3\u0165\3\u0165"+
		"\3\u0166\3\u0166\3\u0167\3\u0167\3\u0168\3\u0168\3\u0169\3\u0169\3\u0169"+
		"\3\u016a\3\u016a\3\u016b\6\u016b\u0f68\n\u016b\r\u016b\16\u016b\u0f69"+
		"\3\u016c\3\u016c\3\u016d\3\u016d\3\u016e\3\u016e\3\u016f\3\u016f\3\u016f"+
		"\3\u0170\3\u0170\3\u0171\3\u0171\3\u0172\3\u0172\3\u0172\3\u0173\3\u0173"+
		"\3\u0174\3\u0174\3\u0175\3\u0175\3\u0176\3\u0176\3\u0177\3\u0177\3\u0178"+
		"\3\u0178\3\u0178\3\u0179\3\u0179\3\u0179\3\u017a\3\u017a\3\u017b\3\u017b"+
		"\3\u017b\3\u017c\3\u017c\3\u017d\3\u017d\3\u017e\3\u017e\3\u017f\3\u017f"+
		"\3\u017f\3\u0180\3\u0180\3\u0181\3\u0181\3\u0182\3\u0182\3\u0182\3\u0183"+
		"\6\u0183\u0fa2\n\u0183\r\u0183\16\u0183\u0fa3\3\u0184\3\u0184\3\u0185"+
		"\3\u0185\3\u0186\3\u0186\3\u0186\3\u0187\3\u0187\3\u0188\3\u0188\5\u0188"+
		"\u0fb1\n\u0188\3\u0189\6\u0189\u0fb4\n\u0189\r\u0189\16\u0189\u0fb5\3"+
		"\u018a\3\u018a\3\u018b\3\u018b\3\u018c\3\u018c\3\u018d\3\u018d\3\u018d"+
		"\3\u018e\3\u018e\3\u018e\3\u018f\3\u018f\3\u0190\6\u0190\u0fc7\n\u0190"+
		"\r\u0190\16\u0190\u0fc8\3\u0191\3\u0191\3\u0192\3\u0192\3\u0193\3\u0193"+
		"\3\u0194\3\u0194\3\u0194\3\u0195\6\u0195\u0fd5\n\u0195\r\u0195\16\u0195"+
		"\u0fd6\3\u0196\3\u0196\3\u0196\3\u0197\3\u0197\3\u0198\3\u0198\3\u0199"+
		"\6\u0199\u0fe1\n\u0199\r\u0199\16\u0199\u0fe2\3\u019a\3\u019a\3\u019a"+
		"\3\u019b\3\u019b\3\u019c\3\u019c\3\u019d\3\u019d\3\u019e\3\u019e\3\u019f"+
		"\3\u019f\3\u01a0\3\u01a0\3\u01a0\3\u01a1\3\u01a1\3\u01a1\5\u01a1\u0ff8"+
		"\n\u01a1\3\u01a1\3\u01a1\3\u01a2\6\u01a2\u0ffd\n\u01a2\r\u01a2\16\u01a2"+
		"\u0ffe\3\u01a3\3\u01a3\3\u01a4\3\u01a4\3\u01a5\3\u01a5\3\u01a6\3\u01a6"+
		"\3\u01a7\3\u01a7\3\u01a8\3\u01a8\3\u01a9\3\u01a9\3\u01aa\3\u01aa\3\u01ab"+
		"\3\u01ab\3\u01ac\3\u01ac\3\u01ad\3\u01ad\3\u01ae\3\u01ae\3\u01af\3\u01af"+
		"\3\u01b0\3\u01b0\3\u01b1\3\u01b1\3\u01b2\3\u01b2\3\u01b3\3\u01b3\3\u01b4"+
		"\3\u01b4\3\u01b5\6\u01b5\u1026\n\u01b5\r\u01b5\16\u01b5\u1027\3\u01b6"+
		"\3\u01b6\3\u01b7\3\u01b7\3\u01b8\3\u01b8\3\u01b8\5\u01b8\u1031\n\u01b8"+
		"\3\u01b8\6\u01b8\u1034\n\u01b8\r\u01b8\16\u01b8\u1035\3\u01b9\3\u01b9"+
		"\3\u01ba\3\u01ba\3\u01bb\3\u01bb\3\u01bc\3\u01bc\5\u01bc\u1040\n\u01bc"+
		"\3\u01bd\3\u01bd\3\u01be\3\u01be\3\u01be\3\u01bf\3\u01bf\3\u01c0\3\u01c0"+
		"\3\u01c1\3\u01c1\3\u01c1\3\u01c2\6\u01c2\u104f\n\u01c2\r\u01c2\16\u01c2"+
		"\u1050\3\u01c3\3\u01c3\3\u01c3\3\u01c4\3\u01c4\3\u01c5\3\u01c5\3\u01c6"+
		"\3\u01c6\3\u01c7\3\u01c7\5\u01c7\u105e\n\u01c7\3\u01c8\3\u01c8\3\u01c8"+
		"\5\u01c8\u1063\n\u01c8\3\u01c8\3\u01c8\3\u01c9\3\u01c9\3\u01ca\3\u01ca"+
		"\3\u01cb\3\u01cb\3\u01cc\3\u01cc\3\u01cd\3\u01cd\3\u01cd\2\2\u01ce\2\4"+
		"\6\b\n\f\16\20\22\24\26\30\32\34\36 \"$&(*,.\60\62\64\668:<>@BDFHJLNP"+
		"RTVXZ\\^`bdfhjlnprtvxz|~\u0080\u0082\u0084\u0086\u0088\u008a\u008c\u008e"+
		"\u0090\u0092\u0094\u0096\u0098\u009a\u009c\u009e\u00a0\u00a2\u00a4\u00a6"+
		"\u00a8\u00aa\u00ac\u00ae\u00b0\u00b2\u00b4\u00b6\u00b8\u00ba\u00bc\u00be"+
		"\u00c0\u00c2\u00c4\u00c6\u00c8\u00ca\u00cc\u00ce\u00d0\u00d2\u00d4\u00d6"+
		"\u00d8\u00da\u00dc\u00de\u00e0\u00e2\u00e4\u00e6\u00e8\u00ea\u00ec\u00ee"+
		"\u00f0\u00f2\u00f4\u00f6\u00f8\u00fa\u00fc\u00fe\u0100\u0102\u0104\u0106"+
		"\u0108\u010a\u010c\u010e\u0110\u0112\u0114\u0116\u0118\u011a\u011c\u011e"+
		"\u0120\u0122\u0124\u0126\u0128\u012a\u012c\u012e\u0130\u0132\u0134\u0136"+
		"\u0138\u013a\u013c\u013e\u0140\u0142\u0144\u0146\u0148\u014a\u014c\u014e"+
		"\u0150\u0152\u0154\u0156\u0158\u015a\u015c\u015e\u0160\u0162\u0164\u0166"+
		"\u0168\u016a\u016c\u016e\u0170\u0172\u0174\u0176\u0178\u017a\u017c\u017e"+
		"\u0180\u0182\u0184\u0186\u0188\u018a\u018c\u018e\u0190\u0192\u0194\u0196"+
		"\u0198\u019a\u019c\u019e\u01a0\u01a2\u01a4\u01a6\u01a8\u01aa\u01ac\u01ae"+
		"\u01b0\u01b2\u01b4\u01b6\u01b8\u01ba\u01bc\u01be\u01c0\u01c2\u01c4\u01c6"+
		"\u01c8\u01ca\u01cc\u01ce\u01d0\u01d2\u01d4\u01d6\u01d8\u01da\u01dc\u01de"+
		"\u01e0\u01e2\u01e4\u01e6\u01e8\u01ea\u01ec\u01ee\u01f0\u01f2\u01f4\u01f6"+
		"\u01f8\u01fa\u01fc\u01fe\u0200\u0202\u0204\u0206\u0208\u020a\u020c\u020e"+
		"\u0210\u0212\u0214\u0216\u0218\u021a\u021c\u021e\u0220\u0222\u0224\u0226"+
		"\u0228\u022a\u022c\u022e\u0230\u0232\u0234\u0236\u0238\u023a\u023c\u023e"+
		"\u0240\u0242\u0244\u0246\u0248\u024a\u024c\u024e\u0250\u0252\u0254\u0256"+
		"\u0258\u025a\u025c\u025e\u0260\u0262\u0264\u0266\u0268\u026a\u026c\u026e"+
		"\u0270\u0272\u0274\u0276\u0278\u027a\u027c\u027e\u0280\u0282\u0284\u0286"+
		"\u0288\u028a\u028c\u028e\u0290\u0292\u0294\u0296\u0298\u029a\u029c\u029e"+
		"\u02a0\u02a2\u02a4\u02a6\u02a8\u02aa\u02ac\u02ae\u02b0\u02b2\u02b4\u02b6"+
		"\u02b8\u02ba\u02bc\u02be\u02c0\u02c2\u02c4\u02c6\u02c8\u02ca\u02cc\u02ce"+
		"\u02d0\u02d2\u02d4\u02d6\u02d8\u02da\u02dc\u02de\u02e0\u02e2\u02e4\u02e6"+
		"\u02e8\u02ea\u02ec\u02ee\u02f0\u02f2\u02f4\u02f6\u02f8\u02fa\u02fc\u02fe"+
		"\u0300\u0302\u0304\u0306\u0308\u030a\u030c\u030e\u0310\u0312\u0314\u0316"+
		"\u0318\u031a\u031c\u031e\u0320\u0322\u0324\u0326\u0328\u032a\u032c\u032e"+
		"\u0330\u0332\u0334\u0336\u0338\u033a\u033c\u033e\u0340\u0342\u0344\u0346"+
		"\u0348\u034a\u034c\u034e\u0350\u0352\u0354\u0356\u0358\u035a\u035c\u035e"+
		"\u0360\u0362\u0364\u0366\u0368\u036a\u036c\u036e\u0370\u0372\u0374\u0376"+
		"\u0378\u037a\u037c\u037e\u0380\u0382\u0384\u0386\u0388\u038a\u038c\u038e"+
		"\u0390\u0392\u0394\u0396\u0398\2\7\4\2;;UV\5\2\4\4\r\r\67\67\5\2\4\4."+
		".WW\5\2\'(CCaa\4\2;;VV\u11a1\2\u0ba8\3\2\2\2\4\u0baa\3\2\2\2\6\u0bad\3"+
		"\2\2\2\b\u0baf\3\2\2\2\n\u0bb1\3\2\2\2\f\u0bb3\3\2\2\2\16\u0bb5\3\2\2"+
		"\2\20\u0bb7\3\2\2\2\22\u0bb9\3\2\2\2\24\u0bbb\3\2\2\2\26\u0bbd\3\2\2\2"+
		"\30\u0bbf\3\2\2\2\32\u0bc2\3\2\2\2\34\u0bc5\3\2\2\2\36\u0bca\3\2\2\2 "+
		"\u0bcd\3\2\2\2\"\u0bcf\3\2\2\2$\u0bd1\3\2\2\2&\u0bd4\3\2\2\2(\u0bd6\3"+
		"\2\2\2*\u0bd8\3\2\2\2,\u0bda\3\2\2\2.\u0bdc\3\2\2\2\60\u0bde\3\2\2\2\62"+
		"\u0be0\3\2\2\2\64\u0be2\3\2\2\2\66\u0be4\3\2\2\28\u0be7\3\2\2\2:\u0be9"+
		"\3\2\2\2<\u0bec\3\2\2\2>\u0bef\3\2\2\2@\u0bf1\3\2\2\2B\u0bf3\3\2\2\2D"+
		"\u0bf6\3\2\2\2F\u0bf8\3\2\2\2H\u0bfb\3\2\2\2J\u0bfd\3\2\2\2L\u0bff\3\2"+
		"\2\2N\u0c01\3\2\2\2P\u0c03\3\2\2\2R\u0c06\3\2\2\2T\u0c0a\3\2\2\2V\u0c0c"+
		"\3\2\2\2X\u0c0f\3\2\2\2Z\u0c12\3\2\2\2\\\u0c16\3\2\2\2^\u0c18\3\2\2\2"+
		"`\u0c1a\3\2\2\2b\u0c1d\3\2\2\2d\u0c1f\3\2\2\2f\u0c22\3\2\2\2h\u0c24\3"+
		"\2\2\2j\u0c26\3\2\2\2l\u0c28\3\2\2\2n\u0c2f\3\2\2\2p\u0c31\3\2\2\2r\u0c34"+
		"\3\2\2\2t\u0c38\3\2\2\2v\u0c3c\3\2\2\2x\u0c3e\3\2\2\2z\u0c40\3\2\2\2|"+
		"\u0c42\3\2\2\2~\u0c44\3\2\2\2\u0080\u0c47\3\2\2\2\u0082\u0c49\3\2\2\2"+
		"\u0084\u0c4b\3\2\2\2\u0086\u0c4d\3\2\2\2\u0088\u0c4f\3\2\2\2\u008a\u0c51"+
		"\3\2\2\2\u008c\u0c54\3\2\2\2\u008e\u0c56\3\2\2\2\u0090\u0c58\3\2\2\2\u0092"+
		"\u0c5b\3\2\2\2\u0094\u0c5f\3\2\2\2\u0096\u0c61\3\2\2\2\u0098\u0c63\3\2"+
		"\2\2\u009a\u0c65\3\2\2\2\u009c\u0c67\3\2\2\2\u009e\u0c69\3\2\2\2\u00a0"+
		"\u0c70\3\2\2\2\u00a2\u0c75\3\2\2\2\u00a4\u0c77\3\2\2\2\u00a6\u0c7b\3\2"+
		"\2\2\u00a8\u0c7d\3\2\2\2\u00aa\u0c80\3\2\2\2\u00ac\u0c82\3\2\2\2\u00ae"+
		"\u0c85\3\2\2\2\u00b0\u0c87\3\2\2\2\u00b2\u0c89\3\2\2\2\u00b4\u0c8b\3\2"+
		"\2\2\u00b6\u0c91\3\2\2\2\u00b8\u0c95\3\2\2\2\u00ba\u0c97\3\2\2\2\u00bc"+
		"\u0c99\3\2\2\2\u00be\u0c9b\3\2\2\2\u00c0\u0c9d\3\2\2\2\u00c2\u0c9f\3\2"+
		"\2\2\u00c4\u0ca1\3\2\2\2\u00c6\u0ca4\3\2\2\2\u00c8\u0ca6\3\2\2\2\u00ca"+
		"\u0ca9\3\2\2\2\u00cc\u0cac\3\2\2\2\u00ce\u0cae\3\2\2\2\u00d0\u0cb0\3\2"+
		"\2\2\u00d2\u0cb3\3\2\2\2\u00d4\u0cb5\3\2\2\2\u00d6\u0cb7\3\2\2\2\u00d8"+
		"\u0cb9\3\2\2\2\u00da\u0cbb\3\2\2\2\u00dc\u0cbe\3\2\2\2\u00de\u0cc1\3\2"+
		"\2\2\u00e0\u0ccd\3\2\2\2\u00e2\u0ccf\3\2\2\2\u00e4\u0cd1\3\2\2\2\u00e6"+
		"\u0cd3\3\2\2\2\u00e8\u0cd5\3\2\2\2\u00ea\u0cd7\3\2\2\2\u00ec\u0cda\3\2"+
		"\2\2\u00ee\u0cdd\3\2\2\2\u00f0\u0ce2\3\2\2\2\u00f2\u0ce4\3\2\2\2\u00f4"+
		"\u0ce6\3\2\2\2\u00f6\u0ce9\3\2\2\2\u00f8\u0cf4\3\2\2\2\u00fa\u0cf6\3\2"+
		"\2\2\u00fc\u0cf8\3\2\2\2\u00fe\u0cfa\3\2\2\2\u0100\u0cfc\3\2\2\2\u0102"+
		"\u0cfe\3\2\2\2\u0104\u0d00\3\2\2\2\u0106\u0d02\3\2\2\2\u0108\u0d05\3\2"+
		"\2\2\u010a\u0d07\3\2\2\2\u010c\u0d09\3\2\2\2\u010e\u0d0b\3\2\2\2\u0110"+
		"\u0d0e\3\2\2\2\u0112\u0d10\3\2\2\2\u0114\u0d12\3\2\2\2\u0116\u0d14\3\2"+
		"\2\2\u0118\u0d17\3\2\2\2\u011a\u0d19\3\2\2\2\u011c\u0d1b\3\2\2\2\u011e"+
		"\u0d1d\3\2\2\2\u0120\u0d1f\3\2\2\2\u0122\u0d21\3\2\2\2\u0124\u0d23\3\2"+
		"\2\2\u0126\u0d25\3\2\2\2\u0128\u0d27\3\2\2\2\u012a\u0d2a\3\2\2\2\u012c"+
		"\u0d2e\3\2\2\2\u012e\u0d30\3\2\2\2\u0130\u0d32\3\2\2\2\u0132\u0d34\3\2"+
		"\2\2\u0134\u0d37\3\2\2\2\u0136\u0d39\3\2\2\2\u0138\u0d3b\3\2\2\2\u013a"+
		"\u0d3d\3\2\2\2\u013c\u0d3f\3\2\2\2\u013e\u0d42\3\2\2\2\u0140\u0d44\3\2"+
		"\2\2\u0142\u0d46\3\2\2\2\u0144\u0d4a\3\2\2\2\u0146\u0d4c\3\2\2\2\u0148"+
		"\u0d4f\3\2\2\2\u014a\u0d51\3\2\2\2\u014c\u0d54\3\2\2\2\u014e\u0d58\3\2"+
		"\2\2\u0150\u0d5a\3\2\2\2\u0152\u0d5d\3\2\2\2\u0154\u0d68\3\2\2\2\u0156"+
		"\u0d6a\3\2\2\2\u0158\u0d6c\3\2\2\2\u015a\u0d6e\3\2\2\2\u015c\u0d71\3\2"+
		"\2\2\u015e\u0d73\3\2\2\2\u0160\u0d76\3\2\2\2\u0162\u0d7a\3\2\2\2\u0164"+
		"\u0d7c\3\2\2\2\u0166\u0d7f\3\2\2\2\u0168\u0d81\3\2\2\2\u016a\u0d83\3\2"+
		"\2\2\u016c\u0d85\3\2\2\2\u016e\u0d88\3\2\2\2\u0170\u0d8a\3\2\2\2\u0172"+
		"\u0d8d\3\2\2\2\u0174\u0d91\3\2\2\2\u0176\u0d93\3\2\2\2\u0178\u0d95\3\2"+
		"\2\2\u017a\u0d98\3\2\2\2\u017c\u0d9c\3\2\2\2\u017e\u0d9e\3\2\2\2\u0180"+
		"\u0da2\3\2\2\2\u0182\u0da9\3\2\2\2\u0184\u0dac\3\2\2\2\u0186\u0db0\3\2"+
		"\2\2\u0188\u0db3\3\2\2\2\u018a\u0db6\3\2\2\2\u018c\u0db9\3\2\2\2\u018e"+
		"\u0dbc\3\2\2\2\u0190\u0dbf\3\2\2\2\u0192\u0dc1\3\2\2\2\u0194\u0dc4\3\2"+
		"\2\2\u0196\u0dc8\3\2\2\2\u0198\u0dcb\3\2\2\2\u019a\u0dcd\3\2\2\2\u019c"+
		"\u0dd0\3\2\2\2\u019e\u0dd2\3\2\2\2\u01a0\u0dd5\3\2\2\2\u01a2\u0dd7\3\2"+
		"\2\2\u01a4\u0dd9\3\2\2\2\u01a6\u0ddb\3\2\2\2\u01a8\u0dde\3\2\2\2\u01aa"+
		"\u0de0\3\2\2\2\u01ac\u0de2\3\2\2\2\u01ae\u0de4\3\2\2\2\u01b0\u0de6\3\2"+
		"\2\2\u01b2\u0de8\3\2\2\2\u01b4\u0dea\3\2\2\2\u01b6\u0ded\3\2\2\2\u01b8"+
		"\u0df0\3\2\2\2\u01ba\u0df2\3\2\2\2\u01bc\u0df4\3\2\2\2\u01be\u0dfc\3\2"+
		"\2\2\u01c0\u0dfe\3\2\2\2\u01c2\u0e01\3\2\2\2\u01c4\u0e03\3\2\2\2\u01c6"+
		"\u0e05\3\2\2\2\u01c8\u0e08\3\2\2\2\u01ca\u0e0a\3\2\2\2\u01cc\u0e0c\3\2"+
		"\2\2\u01ce\u0e0e\3\2\2\2\u01d0\u0e10\3\2\2\2\u01d2\u0e12\3\2\2\2\u01d4"+
		"\u0e15\3\2\2\2\u01d6\u0e17\3\2\2\2\u01d8\u0e1a\3\2\2\2\u01da\u0e1d\3\2"+
		"\2\2\u01dc\u0e1f\3\2\2\2\u01de\u0e22\3\2\2\2\u01e0\u0e24\3\2\2\2\u01e2"+
		"\u0e26\3\2\2\2\u01e4\u0e28\3\2\2\2\u01e6\u0e2a\3\2\2\2\u01e8\u0e2d\3\2"+
		"\2\2\u01ea\u0e30\3\2\2\2\u01ec\u0e33\3\2\2\2\u01ee\u0e35\3\2\2\2\u01f0"+
		"\u0e39\3\2\2\2\u01f2\u0e3c\3\2\2\2\u01f4\u0e3e\3\2\2\2\u01f6\u0e41\3\2"+
		"\2\2\u01f8\u0e44\3\2\2\2\u01fa\u0e47\3\2\2\2\u01fc\u0e4b\3\2\2\2\u01fe"+
		"\u0e4d\3\2\2\2\u0200\u0e4f\3\2\2\2\u0202\u0e53\3\2\2\2\u0204\u0e57\3\2"+
		"\2\2\u0206\u0e59\3\2\2\2\u0208\u0e5c\3\2\2\2\u020a\u0e5e\3\2\2\2\u020c"+
		"\u0e61\3\2\2\2\u020e\u0e63\3\2\2\2\u0210\u0e66\3\2\2\2\u0212\u0e68\3\2"+
		"\2\2\u0214\u0e6a\3\2\2\2\u0216\u0e6c\3\2\2\2\u0218\u0e6e\3\2\2\2\u021a"+
		"\u0e70\3\2\2\2\u021c\u0e73\3\2\2\2\u021e\u0e75\3\2\2\2\u0220\u0e77\3\2"+
		"\2\2\u0222\u0e7e\3\2\2\2\u0224\u0e80\3\2\2\2\u0226\u0e82\3\2\2\2\u0228"+
		"\u0e8b\3\2\2\2\u022a\u0e8d\3\2\2\2\u022c\u0e8f\3\2\2\2\u022e\u0e91\3\2"+
		"\2\2\u0230\u0e93\3\2\2\2\u0232\u0e96\3\2\2\2\u0234\u0e98\3\2\2\2\u0236"+
		"\u0e9a\3\2\2\2\u0238\u0e9c\3\2\2\2\u023a\u0e9e\3\2\2\2\u023c\u0ea0\3\2"+
		"\2\2\u023e\u0ea3\3\2\2\2\u0240\u0ea5\3\2\2\2\u0242\u0ea7\3\2\2\2\u0244"+
		"\u0ea9\3\2\2\2\u0246\u0eab\3\2\2\2\u0248\u0eb4\3\2\2\2\u024a\u0ebb\3\2"+
		"\2\2\u024c\u0ebd\3\2\2\2\u024e\u0ebf\3\2\2\2\u0250\u0ec1\3\2\2\2\u0252"+
		"\u0ec3\3\2\2\2\u0254\u0ec6\3\2\2\2\u0256\u0ec8\3\2\2\2\u0258\u0ecb\3\2"+
		"\2\2\u025a\u0ecd\3\2\2\2\u025c\u0ecf\3\2\2\2\u025e\u0ed1\3\2\2\2\u0260"+
		"\u0ed3\3\2\2\2\u0262\u0ed5\3\2\2\2\u0264\u0ed8\3\2\2\2\u0266\u0eda\3\2"+
		"\2\2\u0268\u0edd\3\2\2\2\u026a\u0edf\3\2\2\2\u026c\u0ee1\3\2\2\2\u026e"+
		"\u0ee3\3\2\2\2\u0270\u0ee5\3\2\2\2\u0272\u0ee8\3\2\2\2\u0274\u0eec\3\2"+
		"\2\2\u0276\u0eef\3\2\2\2\u0278\u0ef1\3\2\2\2\u027a\u0ef4\3\2\2\2\u027c"+
		"\u0ef6\3\2\2\2\u027e\u0ef8\3\2\2\2\u0280\u0efa\3\2\2\2\u0282\u0efe\3\2"+
		"\2\2\u0284\u0f00\3\2\2\2\u0286\u0f02\3\2\2\2\u0288\u0f04\3\2\2\2\u028a"+
		"\u0f06\3\2\2\2\u028c\u0f08\3\2\2\2\u028e\u0f0b\3\2\2\2\u0290\u0f0d\3\2"+
		"\2\2\u0292\u0f0f\3\2\2\2\u0294\u0f11\3\2\2\2\u0296\u0f15\3\2\2\2\u0298"+
		"\u0f17\3\2\2\2\u029a\u0f19\3\2\2\2\u029c\u0f1b\3\2\2\2\u029e\u0f1d\3\2"+
		"\2\2\u02a0\u0f25\3\2\2\2\u02a2\u0f29\3\2\2\2\u02a4\u0f2b\3\2\2\2\u02a6"+
		"\u0f2d\3\2\2\2\u02a8\u0f2f\3\2\2\2\u02aa\u0f36\3\2\2\2\u02ac\u0f38\3\2"+
		"\2\2\u02ae\u0f3b\3\2\2\2\u02b0\u0f3d\3\2\2\2\u02b2\u0f40\3\2\2\2\u02b4"+
		"\u0f44\3\2\2\2\u02b6\u0f47\3\2\2\2\u02b8\u0f49\3\2\2\2\u02ba\u0f4b\3\2"+
		"\2\2\u02bc\u0f4d\3\2\2\2\u02be\u0f4f\3\2\2\2\u02c0\u0f51\3\2\2\2\u02c2"+
		"\u0f53\3\2\2\2\u02c4\u0f55\3\2\2\2\u02c6\u0f57\3\2\2\2\u02c8\u0f59\3\2"+
		"\2\2\u02ca\u0f5b\3\2\2\2\u02cc\u0f5d\3\2\2\2\u02ce\u0f5f\3\2\2\2\u02d0"+
		"\u0f61\3\2\2\2\u02d2\u0f64\3\2\2\2\u02d4\u0f67\3\2\2\2\u02d6\u0f6b\3\2"+
		"\2\2\u02d8\u0f6d\3\2\2\2\u02da\u0f6f\3\2\2\2\u02dc\u0f71\3\2\2\2\u02de"+
		"\u0f74\3\2\2\2\u02e0\u0f76\3\2\2\2\u02e2\u0f78\3\2\2\2\u02e4\u0f7b\3\2"+
		"\2\2\u02e6\u0f7d\3\2\2\2\u02e8\u0f7f\3\2\2\2\u02ea\u0f81\3\2\2\2\u02ec"+
		"\u0f83\3\2\2\2\u02ee\u0f85\3\2\2\2\u02f0\u0f88\3\2\2\2\u02f2\u0f8b\3\2"+
		"\2\2\u02f4\u0f8d\3\2\2\2\u02f6\u0f90\3\2\2\2\u02f8\u0f92\3\2\2\2\u02fa"+
		"\u0f94\3\2\2\2\u02fc\u0f96\3\2\2\2\u02fe\u0f99\3\2\2\2\u0300\u0f9b\3\2"+
		"\2\2\u0302\u0f9d\3\2\2\2\u0304\u0fa1\3\2\2\2\u0306\u0fa5\3\2\2\2\u0308"+
		"\u0fa7\3\2\2\2\u030a\u0fa9\3\2\2\2\u030c\u0fac\3\2\2\2\u030e\u0fae\3\2"+
		"\2\2\u0310\u0fb3\3\2\2\2\u0312\u0fb7\3\2\2\2\u0314\u0fb9\3\2\2\2\u0316"+
		"\u0fbb\3\2\2\2\u0318\u0fbd\3\2\2\2\u031a\u0fc0\3\2\2\2\u031c\u0fc3\3\2"+
		"\2\2\u031e\u0fc6\3\2\2\2\u0320\u0fca\3\2\2\2\u0322\u0fcc\3\2\2\2\u0324"+
		"\u0fce\3\2\2\2\u0326\u0fd0\3\2\2\2\u0328\u0fd4\3\2\2\2\u032a\u0fd8\3\2"+
		"\2\2\u032c\u0fdb\3\2\2\2\u032e\u0fdd\3\2\2\2\u0330\u0fe0\3\2\2\2\u0332"+
		"\u0fe4\3\2\2\2\u0334\u0fe7\3\2\2\2\u0336\u0fe9\3\2\2\2\u0338\u0feb\3\2"+
		"\2\2\u033a\u0fed\3\2\2\2\u033c\u0fef\3\2\2\2\u033e\u0ff1\3\2\2\2\u0340"+
		"\u0ff4\3\2\2\2\u0342\u0ffc\3\2\2\2\u0344\u1000\3\2\2\2\u0346\u1002\3\2"+
		"\2\2\u0348\u1004\3\2\2\2\u034a\u1006\3\2\2\2\u034c\u1008\3\2\2\2\u034e"+
		"\u100a\3\2\2\2\u0350\u100c\3\2\2\2\u0352\u100e\3\2\2\2\u0354\u1010\3\2"+
		"\2\2\u0356\u1012\3\2\2\2\u0358\u1014\3\2\2\2\u035a\u1016\3\2\2\2\u035c"+
		"\u1018\3\2\2\2\u035e\u101a\3\2\2\2\u0360\u101c\3\2\2\2\u0362\u101e\3\2"+
		"\2\2\u0364\u1020\3\2\2\2\u0366\u1022\3\2\2\2\u0368\u1025\3\2\2\2\u036a"+
		"\u1029\3\2\2\2\u036c\u102b\3\2\2\2\u036e\u102d\3\2\2\2\u0370\u1037\3\2"+
		"\2\2\u0372\u1039\3\2\2\2\u0374\u103b\3\2\2\2\u0376\u103d\3\2\2\2\u0378"+
		"\u1041\3\2\2\2\u037a\u1043\3\2\2\2\u037c\u1046\3\2\2\2\u037e\u1048\3\2"+
		"\2\2\u0380\u104a\3\2\2\2\u0382\u104e\3\2\2\2\u0384\u1052\3\2\2\2\u0386"+
		"\u1055\3\2\2\2\u0388\u1057\3\2\2\2\u038a\u1059\3\2\2\2\u038c\u105b\3\2"+
		"\2\2\u038e\u105f\3\2\2\2\u0390\u1066\3\2\2\2\u0392\u1068\3\2\2\2\u0394"+
		"\u106a\3\2\2\2\u0396\u106c\3\2\2\2\u0398\u106e\3\2\2\2\u039a\u039c\7\3"+
		"\2\2\u039b\u039d\5\u0094K\2\u039c\u039b\3\2\2\2\u039c\u039d\3\2\2\2\u039d"+
		"\u039f\3\2\2\2\u039e\u03a0\5\u030c\u0187\2\u039f\u039e\3\2\2\2\u039f\u03a0"+
		"\3\2\2\2\u03a0\u03a2\3\2\2\2\u03a1\u03a3\5v<\2\u03a2\u03a1\3\2\2\2\u03a2"+
		"\u03a3\3\2\2\2\u03a3\u03a5\3\2\2\2\u03a4\u03a6\5\u026a\u0136\2\u03a5\u03a4"+
		"\3\2\2\2\u03a5\u03a6\3\2\2\2\u03a6\u03a8\3\2\2\2\u03a7\u03a9\5\u02da\u016e"+
		"\2\u03a8\u03a7\3\2\2\2\u03a8\u03a9\3\2\2\2\u03a9\u03ab\3\2\2\2\u03aa\u03ac"+
		"\5\u02fe\u0180\2\u03ab\u03aa\3\2\2\2\u03ab\u03ac\3\2\2\2\u03ac\u03ae\3"+
		"\2\2\2\u03ad\u03af\5\u00ecw\2\u03ae\u03ad\3\2\2\2\u03ae\u03af\3\2\2\2"+
		"\u03af\u03b1\3\2\2\2\u03b0\u03b2\7\u00b5\2\2\u03b1\u03b0\3\2\2\2\u03b2"+
		"\u03b3\3\2\2\2\u03b3\u03b1\3\2\2\2\u03b3\u03b4\3\2\2\2\u03b4\u03b6\3\2"+
		"\2\2\u03b5\u03b7\5b\62\2\u03b6\u03b5\3\2\2\2\u03b6\u03b7\3\2\2\2\u03b7"+
		"\u03b9\3\2\2\2\u03b8\u03ba\5\u01bc\u00df\2\u03b9\u03b8\3\2\2\2\u03b9\u03ba"+
		"\3\2\2\2\u03ba\u03bc\3\2\2\2\u03bb\u03bd\5\u02b4\u015b\2\u03bc\u03bb\3"+
		"\2\2\2\u03bc\u03bd\3\2\2\2\u03bd\u03bf\3\2\2\2\u03be\u03c0\5\u01a6\u00d4"+
		"\2\u03bf\u03be\3\2\2\2\u03bf\u03c0\3\2\2\2\u03c0\u03c2\3\2\2\2\u03c1\u03c3"+
		"\5\u01e6\u00f4\2\u03c2\u03c1\3\2\2\2\u03c2\u03c3\3\2\2\2\u03c3\u03c5\3"+
		"\2\2\2\u03c4\u03c6\5\u00c4c\2\u03c5\u03c4\3\2\2\2\u03c5\u03c6\3\2\2\2"+
		"\u03c6\u03c8\3\2\2\2\u03c7\u03c9\5\u00ccg\2\u03c8\u03c7\3\2\2\2\u03c8"+
		"\u03c9\3\2\2\2\u03c9\u03cb\3\2\2\2\u03ca\u03cc\5\u033e\u01a0\2\u03cb\u03ca"+
		"\3\2\2\2\u03cb\u03cc\3\2\2\2\u03cc\u03ce\3\2\2\2\u03cd\u03cf\5\32\16\2"+
		"\u03ce\u03cd\3\2\2\2\u03ce\u03cf\3\2\2\2\u03cf\u03d1\3\2\2\2\u03d0\u03d2"+
		"\5\u0180\u00c1\2\u03d1\u03d0\3\2\2\2\u03d1\u03d2\3\2\2\2\u03d2\u03d4\3"+
		"\2\2\2\u03d3\u03d5\5\u0262\u0132\2\u03d4\u03d3\3\2\2\2\u03d4\u03d5\3\2"+
		"\2\2\u03d5\u03d7\3\2\2\2\u03d6\u03d8\5\u02d0\u0169\2\u03d7\u03d6\3\2\2"+
		"\2\u03d7\u03d8\3\2\2\2\u03d8\u03da\3\2\2\2\u03d9\u03db\5\u02dc\u016f\2"+
		"\u03da\u03d9\3\2\2\2\u03da\u03db\3\2\2\2\u03db\u03dd\3\2\2\2\u03dc\u03de"+
		"\5\u026a\u0136\2\u03dd\u03dc\3\2\2\2\u03dd\u03de\3\2\2\2\u03de\u03e0\3"+
		"\2\2\2\u03df\u03e1\5\u026a\u0136\2\u03e0\u03df\3\2\2\2\u03e0\u03e1\3\2"+
		"\2\2\u03e1\u03e3\3\2\2\2\u03e2\u03e4\5\u0346\u01a4\2\u03e3\u03e2\3\2\2"+
		"\2\u03e3\u03e4\3\2\2\2\u03e4\u03e6\3\2\2\2\u03e5\u03e7\5\u0358\u01ad\2"+
		"\u03e6\u03e5\3\2\2\2\u03e6\u03e7\3\2\2\2\u03e7\u03e9\3\2\2\2\u03e8\u03ea"+
		"\5\u02da\u016e\2\u03e9\u03e8\3\2\2\2\u03e9\u03ea\3\2\2\2\u03ea\u03ec\3"+
		"\2\2\2\u03eb\u03ed\5\u0378\u01bd\2\u03ec\u03eb\3\2\2\2\u03ec\u03ed\3\2"+
		"\2\2\u03ed\u03ef\3\2\2\2\u03ee\u03f0\5\u0346\u01a4\2\u03ef\u03ee\3\2\2"+
		"\2\u03ef\u03f0\3\2\2\2\u03f0\u03f2\3\2\2\2\u03f1\u03f3\5\u0308\u0185\2"+
		"\u03f2\u03f1\3\2\2\2\u03f2\u03f3\3\2\2\2\u03f3\u03f5\3\2\2\2\u03f4\u03f6"+
		"\5\u0378\u01bd\2\u03f5\u03f4\3\2\2\2\u03f5\u03f6\3\2\2\2\u03f6\u03f8\3"+
		"\2\2\2\u03f7\u03f9\5|?\2\u03f8\u03f7\3\2\2\2\u03f8\u03f9\3\2\2\2\u03f9"+
		"\u03fb\3\2\2\2\u03fa\u03fc\5\u0086D\2\u03fb\u03fa\3\2\2\2\u03fb\u03fc"+
		"\3\2\2\2\u03fc\u03fe\3\2\2\2\u03fd\u03ff\5\u0380\u01c1\2\u03fe\u03fd\3"+
		"\2\2\2\u03fe\u03ff\3\2\2\2\u03ff\u0401\3\2\2\2\u0400\u0402\5\\/\2\u0401"+
		"\u0400\3\2\2\2\u0401\u0402\3\2\2\2\u0402\u0404\3\2\2\2\u0403\u0405\5\u038e"+
		"\u01c8\2\u0404\u0403\3\2\2\2\u0404\u0405\3\2\2\2\u0405\u0407\3\2\2\2\u0406"+
		"\u0408\5\u036e\u01b8\2\u0407\u0406\3\2\2\2\u0407\u0408\3\2\2\2\u0408\u040a"+
		"\3\2\2\2\u0409\u040b\5\u0220\u0111\2\u040a\u0409\3\2\2\2\u040a\u040b\3"+
		"\2\2\2\u040b\u040d\3\2\2\2\u040c\u040e\5\u00a0Q\2\u040d\u040c\3\2\2\2"+
		"\u040d\u040e\3\2\2\2\u040e\u0410\3\2\2\2\u040f\u0411\5\u0142\u00a2\2\u0410"+
		"\u040f\3\2\2\2\u0410\u0411\3\2\2\2\u0411\u0413\3\2\2\2\u0412\u0414\5\u0294"+
		"\u014b\2\u0413\u0412\3\2\2\2\u0413\u0414\3\2\2\2\u0414\u0416\3\2\2\2\u0415"+
		"\u0417\5\u0230\u0119\2\u0416\u0415\3\2\2\2\u0416\u0417\3\2\2\2\u0417\u0419"+
		"\3\2\2\2\u0418\u041a\5`\61\2\u0419\u0418\3\2\2\2\u0419\u041a\3\2\2\2\u041a"+
		"\u041c\3\2\2\2\u041b\u041d\5\u016c\u00b7\2\u041c\u041b\3\2\2\2\u041c\u041d"+
		"\3\2\2\2\u041d\u041f\3\2\2\2\u041e\u0420\5$\23\2\u041f\u041e\3\2\2\2\u041f"+
		"\u0420\3\2\2\2\u0420\u0422\3\2\2\2\u0421\u0423\5\u02cc\u0167\2\u0422\u0421"+
		"\3\2\2\2\u0422\u0423\3\2\2\2\u0423\u0425\3\2\2\2\u0424\u0426\5\u01dc\u00ef"+
		"\2\u0425\u0424\3\2\2\2\u0425\u0426\3\2\2\2\u0426\u0428\3\2\2\2\u0427\u0429"+
		"\5\u01dc\u00ef\2\u0428\u0427\3\2\2\2\u0428\u0429\3\2\2\2\u0429\u042b\3"+
		"\2\2\2\u042a\u042c\5\u0116\u008c\2\u042b\u042a\3\2\2\2\u042b\u042c\3\2"+
		"\2\2\u042c\u042e\3\2\2\2\u042d\u042f\5\u00d0i\2\u042e\u042d\3\2\2\2\u042e"+
		"\u042f\3\2\2\2\u042f\u0431\3\2\2\2\u0430\u0432\5\u01c0\u00e1\2\u0431\u0430"+
		"\3\2\2\2\u0431\u0432\3\2\2\2\u0432\u0434\3\2\2\2\u0433\u0435\5\u0196\u00cc"+
		"\2\u0434\u0433\3\2\2\2\u0434\u0435\3\2\2\2\u0435\u0437\3\2\2\2\u0436\u0438"+
		"\5V,\2\u0437\u0436\3\2\2\2\u0437\u0438\3\2\2\2\u0438\u043a\3\2\2\2\u0439"+
		"\u043b\5\u0326\u0194\2\u043a\u0439\3\2\2\2\u043a\u043b\3\2\2\2\u043b\u043d"+
		"\3\2\2\2\u043c\u043e\5\u018a\u00c6\2\u043d\u043c\3\2\2\2\u043d\u043e\3"+
		"\2\2\2\u043e\u0440\3\2\2\2\u043f\u0441\5\u01e2\u00f2\2\u0440\u043f\3\2"+
		"\2\2\u0440\u0441\3\2\2\2\u0441\u0443\3\2\2\2\u0442\u0444\5\u019e\u00d0"+
		"\2\u0443\u0442\3\2\2\2\u0443\u0444\3\2\2\2\u0444\u0446\3\2\2\2\u0445\u0447"+
		"\5\u01d6\u00ec\2\u0446\u0445\3\2\2\2\u0446\u0447\3\2\2\2\u0447\u0449\3"+
		"\2\2\2\u0448\u044a\5\36\20\2\u0449\u0448\3\2\2\2\u0449\u044a\3\2\2\2\u044a"+
		"\u044c\3\2\2\2\u044b\u044d\5\u019a\u00ce\2\u044c\u044b\3\2\2\2\u044c\u044d"+
		"\3\2\2\2\u044d\u044f\3\2\2\2\u044e\u0450\5\u0268\u0135\2\u044f\u044e\3"+
		"\2\2\2\u044f\u0450\3\2\2\2\u0450\u0452\3\2\2\2\u0451\u0453\5\u01b4\u00db"+
		"\2\u0452\u0451\3\2\2\2\u0452\u0453\3\2\2\2\u0453\u0455\3\2\2\2\u0454\u0456"+
		"\5F$\2\u0455\u0454\3\2\2\2\u0455\u0456\3\2\2\2\u0456\u0458\3\2\2\2\u0457"+
		"\u0459\5\u0150\u00a9\2\u0458\u0457\3\2\2\2\u0458\u0459\3\2\2\2\u0459\u045b"+
		"\3\2\2\2\u045a\u045c\5\u0106\u0084\2\u045b\u045a\3\2\2\2\u045b\u045c\3"+
		"\2\2\2\u045c\u045e\3\2\2\2\u045d\u045f\5\u0166\u00b4\2\u045e\u045d\3\2"+
		"\2\2\u045e\u045f\3\2\2\2\u045f\u0461\3\2\2\2\u0460\u0462\5\u0232\u011a"+
		"\2\u0461\u0460\3\2\2\2\u0461\u0462\3\2\2\2\u0462\u0464\3\2\2\2\u0463\u0465"+
		"\5\u02b6\u015c\2\u0464\u0463\3\2\2\2\u0464\u0465\3\2\2\2\u0465\u0467\3"+
		"\2\2\2\u0466\u0468\5\u0210\u0109\2\u0467\u0466\3\2\2\2\u0467\u0468\3\2"+
		"\2\2\u0468\u046a\3\2\2\2\u0469\u046b\5\u0340\u01a1\2\u046a\u0469\3\2\2"+
		"\2\u046a\u046b\3\2\2\2\u046b\u046d\3\2\2\2\u046c\u046e\5l\67\2\u046d\u046c"+
		"\3\2\2\2\u046d\u046e\3\2\2\2\u046e\u0470\3\2\2\2\u046f\u0471\5\u01d2\u00ea"+
		"\2\u0470\u046f\3\2\2\2\u0470\u0471\3\2\2\2\u0471\u0473\3\2\2\2\u0472\u0474"+
		"\5\u00caf\2\u0473\u0472\3\2\2\2\u0473\u0474\3\2\2\2\u0474\u0476\3\2\2"+
		"\2\u0475\u0477\5\u00b6\\\2\u0476\u0475\3\2\2\2\u0476\u0477\3\2\2\2\u0477"+
		"\u0479\3\2\2\2\u0478\u047a\5\u0280\u0141\2\u0479\u0478\3\2\2\2\u0479\u047a"+
		"\3\2\2\2\u047a\u047c\3\2\2\2\u047b\u047d\5\u0192\u00ca\2\u047c\u047b\3"+
		"\2\2\2\u047c\u047d\3\2\2\2\u047d\u047f\3\2\2\2\u047e\u0480\5D#\2\u047f"+
		"\u047e\3\2\2\2\u047f\u0480\3\2\2\2\u0480\u0482\3\2\2\2\u0481\u0483\5\u0200"+
		"\u0101\2\u0482\u0481\3\2\2\2\u0482\u0483\3\2\2\2\u0483\u0485\3\2\2\2\u0484"+
		"\u0486\5\u0082B\2\u0485\u0484\3\2\2\2\u0485\u0486\3\2\2\2\u0486\u0488"+
		"\3\2\2\2\u0487\u0489\5\u010e\u0088\2\u0488\u0487\3\2\2\2\u0488\u0489\3"+
		"\2\2\2\u0489\u048b\3\2\2\2\u048a\u048c\5\u0266\u0134\2\u048b\u048a\3\2"+
		"\2\2\u048b\u048c\3\2\2\2\u048c\u048e\3\2\2\2\u048d\u048f\5\u00eav\2\u048e"+
		"\u048d\3\2\2\2\u048e\u048f\3\2\2\2\u048f\u0491\3\2\2\2\u0490\u0492\5\u00de"+
		"p\2\u0491\u0490\3\2\2\2\u0491\u0492\3\2\2\2\u0492\u0494\3\2\2\2\u0493"+
		"\u0495\5\u029e\u0150\2\u0494\u0493\3\2\2\2\u0494\u0495\3\2\2\2\u0495\u0497"+
		"\3\2\2\2\u0496\u0498\5\u01f0\u00f9\2\u0497\u0496\3\2\2\2\u0497\u0498\3"+
		"\2\2\2\u0498\u049a\3\2\2\2\u0499\u049b\5\u0318\u018d\2\u049a\u0499\3\2"+
		"\2\2\u049a\u049b\3\2\2\2\u049b\u049d\3\2\2\2\u049c\u049e\5\u00dan\2\u049d"+
		"\u049c\3\2\2\2\u049d\u049e\3\2\2\2\u049e\u04a0\3\2\2\2\u049f\u04a1\5\u02e6"+
		"\u0174\2\u04a0\u049f\3\2\2\2\u04a0\u04a1\3\2\2\2\u04a1\u04a3\3\2\2\2\u04a2"+
		"\u04a4\5\u020a\u0106\2\u04a3\u04a2\3\2\2\2\u04a3\u04a4\3\2\2\2\u04a4\u04a6"+
		"\3\2\2\2\u04a5\u04a7\5^\60\2\u04a6\u04a5\3\2\2\2\u04a6\u04a7\3\2\2\2\u04a7"+
		"\u04a9\3\2\2\2\u04a8\u04aa\5\u02c6\u0164\2\u04a9\u04a8\3\2\2\2\u04a9\u04aa"+
		"\3\2\2\2\u04aa\u04ac\3\2\2\2\u04ab\u04ad\5\u00c6d\2\u04ac\u04ab\3\2\2"+
		"\2\u04ac\u04ad\3\2\2\2\u04ad\u04af\3\2\2\2\u04ae\u04b0\5\u0152\u00aa\2"+
		"\u04af\u04ae\3\2\2\2\u04af\u04b0\3\2\2\2\u04b0\u0ba9\3\2\2\2\u04b1\u04b3"+
		"\7\3\2\2\u04b2\u04b4\5\u0094K\2\u04b3\u04b2\3\2\2\2\u04b3\u04b4\3\2\2"+
		"\2\u04b4\u04b6\3\2\2\2\u04b5\u04b7\5\u030c\u0187\2\u04b6\u04b5\3\2\2\2"+
		"\u04b6\u04b7\3\2\2\2\u04b7\u04b9\3\2\2\2\u04b8\u04ba\5v<\2\u04b9\u04b8"+
		"\3\2\2\2\u04b9\u04ba\3\2\2\2\u04ba\u04bc\3\2\2\2\u04bb\u04bd\5\u026a\u0136"+
		"\2\u04bc\u04bb\3\2\2\2\u04bc\u04bd\3\2\2\2\u04bd\u04bf\3\2\2\2\u04be\u04c0"+
		"\5\u02da\u016e\2\u04bf\u04be\3\2\2\2\u04bf\u04c0\3\2\2\2\u04c0\u04c2\3"+
		"\2\2\2\u04c1\u04c3\5\u02fe\u0180\2\u04c2\u04c1\3\2\2\2\u04c2\u04c3\3\2"+
		"\2\2\u04c3\u04c4\3\2\2\2\u04c4\u04c5\7\4\2\2\u04c5\u04c7\7\u00b5\2\2\u04c6"+
		"\u04c8\5R*\2\u04c7\u04c6\3\2\2\2\u04c7\u04c8\3\2\2\2\u04c8\u04ca\3\2\2"+
		"\2\u04c9\u04cb\5b\62\2\u04ca\u04c9\3\2\2\2\u04ca\u04cb\3\2\2\2\u04cb\u04cd"+
		"\3\2\2\2\u04cc\u04ce\5\u01bc\u00df\2\u04cd\u04cc\3\2\2\2\u04cd\u04ce\3"+
		"\2\2\2\u04ce\u04d0\3\2\2\2\u04cf\u04d1\5\u02b4\u015b\2\u04d0\u04cf\3\2"+
		"\2\2\u04d0\u04d1\3\2\2\2\u04d1\u04d3\3\2\2\2\u04d2\u04d4\5\u01a6\u00d4"+
		"\2\u04d3\u04d2\3\2\2\2\u04d3\u04d4\3\2\2\2\u04d4\u04d6\3\2\2\2\u04d5\u04d7"+
		"\5\u01e6\u00f4\2\u04d6\u04d5\3\2\2\2\u04d6\u04d7\3\2\2\2\u04d7\u04d9\3"+
		"\2\2\2\u04d8\u04da\5\u00c4c\2\u04d9\u04d8\3\2\2\2\u04d9\u04da\3\2\2\2"+
		"\u04da\u04dc\3\2\2\2\u04db\u04dd\5\u00ccg\2\u04dc\u04db\3\2\2\2\u04dc"+
		"\u04dd\3\2\2\2\u04dd\u04df\3\2\2\2\u04de\u04e0\5\u033e\u01a0\2\u04df\u04de"+
		"\3\2\2\2\u04df\u04e0\3\2\2\2\u04e0\u04e2\3\2\2\2\u04e1\u04e3\5\32\16\2"+
		"\u04e2\u04e1\3\2\2\2\u04e2\u04e3\3\2\2\2\u04e3\u04e5\3\2\2\2\u04e4\u04e6"+
		"\5\u0180\u00c1\2\u04e5\u04e4\3\2\2\2\u04e5\u04e6\3\2\2\2\u04e6\u04e8\3"+
		"\2\2\2\u04e7\u04e9\5\u0262\u0132\2\u04e8\u04e7\3\2\2\2\u04e8\u04e9\3\2"+
		"\2\2\u04e9\u04eb\3\2\2\2\u04ea\u04ec\5\u02d0\u0169\2\u04eb\u04ea\3\2\2"+
		"\2\u04eb\u04ec\3\2\2\2\u04ec\u04ee\3\2\2\2\u04ed\u04ef\5\u02dc\u016f\2"+
		"\u04ee\u04ed\3\2\2\2\u04ee\u04ef\3\2\2\2\u04ef\u04f1\3\2\2\2\u04f0\u04f2"+
		"\5\u026a\u0136\2\u04f1\u04f0\3\2\2\2\u04f1\u04f2\3\2\2\2\u04f2\u04f4\3"+
		"\2\2\2\u04f3\u04f5\5\u026a\u0136\2\u04f4\u04f3\3\2\2\2\u04f4\u04f5\3\2"+
		"\2\2\u04f5\u04f7\3\2\2\2\u04f6\u04f8\5\u0346\u01a4\2\u04f7\u04f6\3\2\2"+
		"\2\u04f7\u04f8\3\2\2\2\u04f8\u04fa\3\2\2\2\u04f9\u04fb\5\u0358\u01ad\2"+
		"\u04fa\u04f9\3\2\2\2\u04fa\u04fb\3\2\2\2\u04fb\u04fd\3\2\2\2\u04fc\u04fe"+
		"\5\u02da\u016e\2\u04fd\u04fc\3\2\2\2\u04fd\u04fe\3\2\2\2\u04fe\u0500\3"+
		"\2\2\2\u04ff\u0501\5\u0378\u01bd\2\u0500\u04ff\3\2\2\2\u0500\u0501\3\2"+
		"\2\2\u0501\u0503\3\2\2\2\u0502\u0504\5\u0346\u01a4\2\u0503\u0502\3\2\2"+
		"\2\u0503\u0504\3\2\2\2\u0504\u0506\3\2\2\2\u0505\u0507\5\u0308\u0185\2"+
		"\u0506\u0505\3\2\2\2\u0506\u0507\3\2\2\2\u0507\u0509\3\2\2\2\u0508\u050a"+
		"\5\u0378\u01bd\2\u0509\u0508\3\2\2\2\u0509\u050a\3\2\2\2\u050a\u050c\3"+
		"\2\2\2\u050b\u050d\5|?\2\u050c\u050b\3\2\2\2\u050c\u050d\3\2\2\2\u050d"+
		"\u050f\3\2\2\2\u050e\u0510\5\u0086D\2\u050f\u050e\3\2\2\2\u050f\u0510"+
		"\3\2\2\2\u0510\u0512\3\2\2\2\u0511\u0513\5\u0380\u01c1\2\u0512\u0511\3"+
		"\2\2\2\u0512\u0513\3\2\2\2\u0513\u0515\3\2\2\2\u0514\u0516\5\\/\2\u0515"+
		"\u0514\3\2\2\2\u0515\u0516\3\2\2\2\u0516\u0518\3\2\2\2\u0517\u0519\5\u038e"+
		"\u01c8\2\u0518\u0517\3\2\2\2\u0518\u0519\3\2\2\2\u0519\u051b\3\2\2\2\u051a"+
		"\u051c\5\u036e\u01b8\2\u051b\u051a\3\2\2\2\u051b\u051c\3\2\2\2\u051c\u051e"+
		"\3\2\2\2\u051d\u051f\5\u0220\u0111\2\u051e\u051d\3\2\2\2\u051e\u051f\3"+
		"\2\2\2\u051f\u0521\3\2\2\2\u0520\u0522\5\u00a0Q\2\u0521\u0520\3\2\2\2"+
		"\u0521\u0522\3\2\2\2\u0522\u0524\3\2\2\2\u0523\u0525\5\u0142\u00a2\2\u0524"+
		"\u0523\3\2\2\2\u0524\u0525\3\2\2\2\u0525\u0527\3\2\2\2\u0526\u0528\5\u0294"+
		"\u014b\2\u0527\u0526\3\2\2\2\u0527\u0528\3\2\2\2\u0528\u052a\3\2\2\2\u0529"+
		"\u052b\5\u0230\u0119\2\u052a\u0529\3\2\2\2\u052a\u052b\3\2\2\2\u052b\u052d"+
		"\3\2\2\2\u052c\u052e\5`\61\2\u052d\u052c\3\2\2\2\u052d\u052e\3\2\2\2\u052e"+
		"\u0530\3\2\2\2\u052f\u0531\5\u016c\u00b7\2\u0530\u052f\3\2\2\2\u0530\u0531"+
		"\3\2\2\2\u0531\u0533\3\2\2\2\u0532\u0534\5$\23\2\u0533\u0532\3\2\2\2\u0533"+
		"\u0534\3\2\2\2\u0534\u0536\3\2\2\2\u0535\u0537\5\u02cc\u0167\2\u0536\u0535"+
		"\3\2\2\2\u0536\u0537\3\2\2\2\u0537\u0539\3\2\2\2\u0538\u053a\5\u01dc\u00ef"+
		"\2\u0539\u0538\3\2\2\2\u0539\u053a\3\2\2\2\u053a\u053c\3\2\2\2\u053b\u053d"+
		"\5\u01dc\u00ef\2\u053c\u053b\3\2\2\2\u053c\u053d\3\2\2\2\u053d\u053f\3"+
		"\2\2\2\u053e\u0540\5\u0116\u008c\2\u053f\u053e\3\2\2\2\u053f\u0540\3\2"+
		"\2\2\u0540\u0542\3\2\2\2\u0541\u0543\5\u00d0i\2\u0542\u0541\3\2\2\2\u0542"+
		"\u0543\3\2\2\2\u0543\u0545\3\2\2\2\u0544\u0546\5\u01c0\u00e1\2\u0545\u0544"+
		"\3\2\2\2\u0545\u0546\3\2\2\2\u0546\u0548\3\2\2\2\u0547\u0549\5\u0196\u00cc"+
		"\2\u0548\u0547\3\2\2\2\u0548\u0549\3\2\2\2\u0549\u054b\3\2\2\2\u054a\u054c"+
		"\5V,\2\u054b\u054a\3\2\2\2\u054b\u054c\3\2\2\2\u054c\u054e\3\2\2\2\u054d"+
		"\u054f\5\u0326\u0194\2\u054e\u054d\3\2\2\2\u054e\u054f\3\2\2\2\u054f\u0551"+
		"\3\2\2\2\u0550\u0552\5\u018a\u00c6\2\u0551\u0550\3\2\2\2\u0551\u0552\3"+
		"\2\2\2\u0552\u0554\3\2\2\2\u0553\u0555\5\u01e2\u00f2\2\u0554\u0553\3\2"+
		"\2\2\u0554\u0555\3\2\2\2\u0555\u0557\3\2\2\2\u0556\u0558\5\u019e\u00d0"+
		"\2\u0557\u0556\3\2\2\2\u0557\u0558\3\2\2\2\u0558\u055a\3\2\2\2\u0559\u055b"+
		"\5\u01d6\u00ec\2\u055a\u0559\3\2\2\2\u055a\u055b\3\2\2\2\u055b\u055d\3"+
		"\2\2\2\u055c\u055e\5\36\20\2\u055d\u055c\3\2\2\2\u055d\u055e\3\2\2\2\u055e"+
		"\u0560\3\2\2\2\u055f\u0561\5\u019a\u00ce\2\u0560\u055f\3\2\2\2\u0560\u0561"+
		"\3\2\2\2\u0561\u0563\3\2\2\2\u0562\u0564\5\u0268\u0135\2\u0563\u0562\3"+
		"\2\2\2\u0563\u0564\3\2\2\2\u0564\u0566\3\2\2\2\u0565\u0567\5\u01b4\u00db"+
		"\2\u0566\u0565\3\2\2\2\u0566\u0567\3\2\2\2\u0567\u0569\3\2\2\2\u0568\u056a"+
		"\5F$\2\u0569\u0568\3\2\2\2\u0569\u056a\3\2\2\2\u056a\u056c\3\2\2\2\u056b"+
		"\u056d\5\u0150\u00a9\2\u056c\u056b\3\2\2\2\u056c\u056d\3\2\2\2\u056d\u056f"+
		"\3\2\2\2\u056e\u0570\5\u0106\u0084\2\u056f\u056e\3\2\2\2\u056f\u0570\3"+
		"\2\2\2\u0570\u0572\3\2\2\2\u0571\u0573\5\u0166\u00b4\2\u0572\u0571\3\2"+
		"\2\2\u0572\u0573\3\2\2\2\u0573\u0575\3\2\2\2\u0574\u0576\5\u0232\u011a"+
		"\2\u0575\u0574\3\2\2\2\u0575\u0576\3\2\2\2\u0576\u0578\3\2\2\2\u0577\u0579"+
		"\5\u02b6\u015c\2\u0578\u0577\3\2\2\2\u0578\u0579\3\2\2\2\u0579\u057b\3"+
		"\2\2\2\u057a\u057c\5\u0210\u0109\2\u057b\u057a\3\2\2\2\u057b\u057c\3\2"+
		"\2\2\u057c\u057e\3\2\2\2\u057d\u057f\5\u0340\u01a1\2\u057e\u057d\3\2\2"+
		"\2\u057e\u057f\3\2\2\2\u057f\u0581\3\2\2\2\u0580\u0582\5l\67\2\u0581\u0580"+
		"\3\2\2\2\u0581\u0582\3\2\2\2\u0582\u0584\3\2\2\2\u0583\u0585\5\u01d2\u00ea"+
		"\2\u0584\u0583\3\2\2\2\u0584\u0585\3\2\2\2\u0585\u0587\3\2\2\2\u0586\u0588"+
		"\5\u00caf\2\u0587\u0586\3\2\2\2\u0587\u0588\3\2\2\2\u0588\u058a\3\2\2"+
		"\2\u0589\u058b\5\u00b6\\\2\u058a\u0589\3\2\2\2\u058a\u058b\3\2\2\2\u058b"+
		"\u058d\3\2\2\2\u058c\u058e\5\u0280\u0141\2\u058d\u058c\3\2\2\2\u058d\u058e"+
		"\3\2\2\2\u058e\u0590\3\2\2\2\u058f\u0591\5\u0192\u00ca\2\u0590\u058f\3"+
		"\2\2\2\u0590\u0591\3\2\2\2\u0591\u0593\3\2\2\2\u0592\u0594\5D#\2\u0593"+
		"\u0592\3\2\2\2\u0593\u0594\3\2\2\2\u0594\u0596\3\2\2\2\u0595\u0597\5\u0200"+
		"\u0101\2\u0596\u0595\3\2\2\2\u0596\u0597\3\2\2\2\u0597\u0599\3\2\2\2\u0598"+
		"\u059a\5\u0082B\2\u0599\u0598\3\2\2\2\u0599\u059a\3\2\2\2\u059a\u059c"+
		"\3\2\2\2\u059b\u059d\5\u010e\u0088\2\u059c\u059b\3\2\2\2\u059c\u059d\3"+
		"\2\2\2\u059d\u059f\3\2\2\2\u059e\u05a0\5\u0266\u0134\2\u059f\u059e\3\2"+
		"\2\2\u059f\u05a0\3\2\2\2\u05a0\u05a2\3\2\2\2\u05a1\u05a3\5\u00eav\2\u05a2"+
		"\u05a1\3\2\2\2\u05a2\u05a3\3\2\2\2\u05a3\u05a5\3\2\2\2\u05a4\u05a6\5\u00de"+
		"p\2\u05a5\u05a4\3\2\2\2\u05a5\u05a6\3\2\2\2\u05a6\u05a8\3\2\2\2\u05a7"+
		"\u05a9\5\u029e\u0150\2\u05a8\u05a7\3\2\2\2\u05a8\u05a9\3\2\2\2\u05a9\u05ab"+
		"\3\2\2\2\u05aa\u05ac\5\u01f0\u00f9\2\u05ab\u05aa\3\2\2\2\u05ab\u05ac\3"+
		"\2\2\2\u05ac\u05ae\3\2\2\2\u05ad\u05af\5\u0318\u018d\2\u05ae\u05ad\3\2"+
		"\2\2\u05ae\u05af\3\2\2\2\u05af\u05b1\3\2\2\2\u05b0\u05b2\5\u00dan\2\u05b1"+
		"\u05b0\3\2\2\2\u05b1\u05b2\3\2\2\2\u05b2\u05b4\3\2\2\2\u05b3\u05b5\5\u02e6"+
		"\u0174\2\u05b4\u05b3\3\2\2\2\u05b4\u05b5\3\2\2\2\u05b5\u05b7\3\2\2\2\u05b6"+
		"\u05b8\5\u020a\u0106\2\u05b7\u05b6\3\2\2\2\u05b7\u05b8\3\2\2\2\u05b8\u05ba"+
		"\3\2\2\2\u05b9\u05bb\5^\60\2\u05ba\u05b9\3\2\2\2\u05ba\u05bb\3\2\2\2\u05bb"+
		"\u05bd\3\2\2\2\u05bc\u05be\5\u02c6\u0164\2\u05bd\u05bc\3\2\2\2\u05bd\u05be"+
		"\3\2\2\2\u05be\u05c0\3\2\2\2\u05bf\u05c1\5\u00c6d\2\u05c0\u05bf\3\2\2"+
		"\2\u05c0\u05c1\3\2\2\2\u05c1\u05c3\3\2\2\2\u05c2\u05c4\5\u0152\u00aa\2"+
		"\u05c3\u05c2\3\2\2\2\u05c3\u05c4\3\2\2\2\u05c4\u0ba9\3\2\2\2\u05c5\u05c7"+
		"\7\5\2\2\u05c6\u05c8\5\u0218\u010d\2\u05c7\u05c6\3\2\2\2\u05c7\u05c8\3"+
		"\2\2\2\u05c8\u05ca\3\2\2\2\u05c9\u05cb\5\u01d4\u00eb\2\u05ca\u05c9\3\2"+
		"\2\2\u05ca\u05cb\3\2\2\2\u05cb\u05cc\3\2\2\2\u05cc\u05cd\7\u00b5\2\2\u05cd"+
		"\u0ba9\7\u00b5\2\2\u05ce\u05d0\7\5\2\2\u05cf\u05d1\5\u0218\u010d\2\u05d0"+
		"\u05cf\3\2\2\2\u05d0\u05d1\3\2\2\2\u05d1\u05d3\3\2\2\2\u05d2\u05d4\5\u01d4"+
		"\u00eb\2\u05d3\u05d2\3\2\2\2\u05d3\u05d4\3\2\2\2\u05d4\u05d6\3\2\2\2\u05d5"+
		"\u05d7\7\u00b5\2\2\u05d6\u05d5\3\2\2\2\u05d7\u05d8\3\2\2\2\u05d8\u05d6"+
		"\3\2\2\2\u05d8\u05d9\3\2\2\2\u05d9\u05da\3\2\2\2\u05da\u0ba9\7\u00b5\2"+
		"\2\u05db\u05dd\7\6\2\2\u05dc\u05de\5\u0198\u00cd\2\u05dd\u05dc\3\2\2\2"+
		"\u05dd\u05de\3\2\2\2\u05de\u05e0\3\2\2\2\u05df\u05e1\5\u0114\u008b\2\u05e0"+
		"\u05df\3\2\2\2\u05e0\u05e1\3\2\2\2\u05e1\u05e3\3\2\2\2\u05e2\u05e4\5\16"+
		"\b\2\u05e3\u05e2\3\2\2\2\u05e3\u05e4\3\2\2\2\u05e4\u05e6\3\2\2\2\u05e5"+
		"\u05e7\5\u0312\u018a\2\u05e6\u05e5\3\2\2\2\u05e6\u05e7\3\2\2\2\u05e7\u05e9"+
		"\3\2\2\2\u05e8\u05ea\5\u0236\u011c\2\u05e9\u05e8\3\2\2\2\u05e9\u05ea\3"+
		"\2\2\2\u05ea\u05ec\3\2\2\2\u05eb\u05ed\5\26\f\2\u05ec\u05eb\3\2\2\2\u05ec"+
		"\u05ed\3\2\2\2\u05ed\u05ef\3\2\2\2\u05ee\u05f0\5\u02c0\u0161\2\u05ef\u05ee"+
		"\3\2\2\2\u05ef\u05f0\3\2\2\2\u05f0\u05f2\3\2\2\2\u05f1\u05f3\5\u0250\u0129"+
		"\2\u05f2\u05f1\3\2\2\2\u05f2\u05f3\3\2\2\2\u05f3\u05f5\3\2\2\2\u05f4\u05f6"+
		"\5\u0334\u019b\2\u05f5\u05f4\3\2\2\2\u05f5\u05f6\3\2\2\2\u05f6\u05f8\3"+
		"\2\2\2\u05f7\u05f9\5T+\2\u05f8\u05f7\3\2\2\2\u05f8\u05f9\3\2\2\2\u05f9"+
		"\u05fb\3\2\2\2\u05fa\u05fc\5\u01ae\u00d8\2\u05fb\u05fa\3\2\2\2\u05fb\u05fc"+
		"\3\2\2\2\u05fc\u05fe\3\2\2\2\u05fd\u05ff\5\u0084C\2\u05fe\u05fd\3\2\2"+
		"\2\u05fe\u05ff\3\2\2\2\u05ff\u0601\3\2\2\2\u0600\u0602\5\u02d6\u016c\2"+
		"\u0601\u0600\3\2\2\2\u0601\u0602\3\2\2\2\u0602\u0604\3\2\2\2\u0603\u0605"+
		"\5\u01de\u00f0\2\u0604\u0603\3\2\2\2\u0604\u0605\3\2\2\2\u0605\u0607\3"+
		"\2\2\2\u0606\u0608\5\u00f0y\2\u0607\u0606\3\2\2\2\u0607\u0608\3\2\2\2"+
		"\u0608\u060a\3\2\2\2\u0609\u060b\5&\24\2\u060a\u0609\3\2\2\2\u060a\u060b"+
		"\3\2\2\2\u060b\u060d\3\2\2\2\u060c\u060e\5\u0306\u0184\2\u060d\u060c\3"+
		"\2\2\2\u060d\u060e\3\2\2\2\u060e\u0610\3\2\2\2\u060f\u0611\5\u0286\u0144"+
		"\2\u0610\u060f\3\2\2\2\u0610\u0611\3\2\2\2\u0611\u0613\3\2\2\2\u0612\u0614"+
		"\5\u0160\u00b1\2\u0613\u0612\3\2\2\2\u0613\u0614\3\2\2\2\u0614\u0ba9\3"+
		"\2\2\2\u0615\u0617\7\7\2\2\u0616\u0618\5\u0264\u0133\2\u0617\u0616\3\2"+
		"\2\2\u0617\u0618\3\2\2\2\u0618\u061a\3\2\2\2\u0619\u061b\5\u0168\u00b5"+
		"\2\u061a\u0619\3\2\2\2\u061a\u061b\3\2\2\2\u061b\u061d\3\2\2\2\u061c\u061e"+
		"\5\u00d4k\2\u061d\u061c\3\2\2\2\u061d\u061e\3\2\2\2\u061e\u0620\3\2\2"+
		"\2\u061f\u0621\5\u035a\u01ae\2\u0620\u061f\3\2\2\2\u0620\u0621\3\2\2\2"+
		"\u0621\u0623\3\2\2\2\u0622\u0624\5\u01ec\u00f7\2\u0623\u0622\3\2\2\2\u0623"+
		"\u0624\3\2\2\2\u0624\u0626\3\2\2\2\u0625\u0627\5\u00fc\177\2\u0626\u0625"+
		"\3\2\2\2\u0626\u0627\3\2\2\2\u0627\u0629\3\2\2\2\u0628\u062a\5n8\2\u0629"+
		"\u0628\3\2\2\2\u0629\u062a\3\2\2\2\u062a\u062c\3\2\2\2\u062b\u062d\5\u02d2"+
		"\u016a\2\u062c\u062b\3\2\2\2\u062c\u062d\3\2\2\2\u062d\u062f\3\2\2\2\u062e"+
		"\u0630\5\u035e\u01b0\2\u062f\u062e\3\2\2\2\u062f\u0630\3\2\2\2\u0630\u0632"+
		"\3\2\2\2\u0631\u0633\5\u02ce\u0168\2\u0632\u0631\3\2\2\2\u0632\u0633\3"+
		"\2\2\2\u0633\u0635\3\2\2\2\u0634\u0636\5\u02f6\u017c\2\u0635\u0634\3\2"+
		"\2\2\u0635\u0636\3\2\2\2\u0636\u0638\3\2\2\2\u0637\u0639\5\u0392\u01ca"+
		"\2\u0638\u0637\3\2\2\2\u0638\u0639\3\2\2\2\u0639\u063b\3\2\2\2\u063a\u063c"+
		"\5\u00b8]\2\u063b\u063a\3\2\2\2\u063b\u063c\3\2\2\2\u063c\u063e\3\2\2"+
		"\2\u063d\u063f\5\u01ce\u00e8\2\u063e\u063d\3\2\2\2\u063e\u063f\3\2\2\2"+
		"\u063f\u0641\3\2\2\2\u0640\u0642\5\u0148\u00a5\2\u0641\u0640\3\2\2\2\u0641"+
		"\u0642\3\2\2\2\u0642\u0644\3\2\2\2\u0643\u0645\5\b\5\2\u0644\u0643\3\2"+
		"\2\2\u0644\u0645\3\2\2\2\u0645\u0647\3\2\2\2\u0646\u0648\5\u02ca\u0166"+
		"\2\u0647\u0646\3\2\2\2\u0647\u0648\3\2\2\2\u0648\u064a\3\2\2\2\u0649\u064b"+
		"\5\u021e\u0110\2\u064a\u0649\3\2\2\2\u064a\u064b\3\2\2\2\u064b\u064d\3"+
		"\2\2\2\u064c\u064e\5\u01c4\u00e3\2\u064d\u064c\3\2\2\2\u064d\u064e\3\2"+
		"\2\2\u064e\u0650\3\2\2\2\u064f\u0651\5\u00c2b\2\u0650\u064f\3\2\2\2\u0650"+
		"\u0651\3\2\2\2\u0651\u0653\3\2\2\2\u0652\u0654\5\u020c\u0107\2\u0653\u0652"+
		"\3\2\2\2\u0653\u0654\3\2\2\2\u0654\u0656\3\2\2\2\u0655\u0657\5\u0322\u0192"+
		"\2\u0656\u0655\3\2\2\2\u0656\u0657\3\2\2\2\u0657\u0659\3\2\2\2\u0658\u065a"+
		"\5\u00a2R\2\u0659\u0658\3\2\2\2\u0659\u065a\3\2\2\2\u065a\u065c\3\2\2"+
		"\2\u065b\u065d\5\u0176\u00bc\2\u065c\u065b\3\2\2\2\u065c\u065d\3\2\2\2"+
		"\u065d\u065f\3\2\2\2\u065e\u0660\5\u028e\u0148\2\u065f\u065e\3\2\2\2\u065f"+
		"\u0660\3\2\2\2\u0660\u0662\3\2\2\2\u0661\u0663\5\u0386\u01c4\2\u0662\u0661"+
		"\3\2\2\2\u0662\u0663\3\2\2\2\u0663\u0665\3\2\2\2\u0664\u0666\5\u02ea\u0176"+
		"\2\u0665\u0664\3\2\2\2\u0665\u0666\3\2\2\2\u0666\u0668\3\2\2\2\u0667\u0669"+
		"\5\u022e\u0118\2\u0668\u0667\3\2\2\2\u0668\u0669\3\2\2\2\u0669\u066b\3"+
		"\2\2\2\u066a\u066c\5\u00f6|\2\u066b\u066a\3\2\2\2\u066b\u066c\3\2\2\2"+
		"\u066c\u066e\3\2\2\2\u066d\u066f\5h\65\2\u066e\u066d\3\2\2\2\u066e\u066f"+
		"\3\2\2\2\u066f\u0671\3\2\2\2\u0670\u0672\5\u0164\u00b3\2\u0671\u0670\3"+
		"\2\2\2\u0671\u0672\3\2\2\2\u0672\u0674\3\2\2\2\u0673\u0675\5\u031a\u018e"+
		"\2\u0674\u0673\3\2\2\2\u0674\u0675\3\2\2\2\u0675\u0677\3\2\2\2\u0676\u0678"+
		"\5\u0132\u009a\2\u0677\u0676\3\2\2\2\u0677\u0678\3\2\2\2\u0678\u067a\3"+
		"\2\2\2\u0679\u067b\5\u023c\u011f\2\u067a\u0679\3\2\2\2\u067a\u067b\3\2"+
		"\2\2\u067b\u067d\3\2\2\2\u067c\u067e\5\u021a\u010e\2\u067d\u067c\3\2\2"+
		"\2\u067d\u067e\3\2\2\2\u067e\u0680\3\2\2\2\u067f\u0681\5\u02a8\u0155\2"+
		"\u0680\u067f\3\2\2\2\u0680\u0681\3\2\2\2\u0681\u0683\3\2\2\2\u0682\u0684"+
		"\5x=\2\u0683\u0682\3\2\2\2\u0683\u0684\3\2\2\2\u0684\u0686\3\2\2\2\u0685"+
		"\u0687\5\u0118\u008d\2\u0686\u0685\3\2\2\2\u0686\u0687\3\2\2\2\u0687\u0689"+
		"\3\2\2\2\u0688\u068a\5\u0214\u010b\2\u0689\u0688\3\2\2\2\u0689\u068a\3"+
		"\2\2\2\u068a\u068c\3\2\2\2\u068b\u068d\5\u009cO\2\u068c\u068b\3\2\2\2"+
		"\u068c\u068d\3\2\2\2\u068d\u068f\3\2\2\2\u068e\u0690\5\u02a0\u0151\2\u068f"+
		"\u068e\3\2\2\2\u068f\u0690\3\2\2\2\u0690\u0ba9\3\2\2\2\u0691\u0693\7\b"+
		"\2\2\u0692\u0694\5.\30\2\u0693\u0692\3\2\2\2\u0693\u0694\3\2\2\2\u0694"+
		"\u0696\3\2\2\2\u0695\u0697\5\u010c\u0087\2\u0696\u0695\3\2\2\2\u0696\u0697"+
		"\3\2\2\2\u0697\u0699\3\2\2\2\u0698\u069a\5\u023e\u0120\2\u0699\u0698\3"+
		"\2\2\2\u0699\u069a\3\2\2\2\u069a\u069c\3\2\2\2\u069b\u069d\5\u02f8\u017d"+
		"\2\u069c\u069b\3\2\2\2\u069c\u069d\3\2\2\2\u069d\u069f\3\2\2\2\u069e\u06a0"+
		"\5\u0352\u01aa\2\u069f\u069e\3\2\2\2\u069f\u06a0\3\2\2\2\u06a0\u06a2\3"+
		"\2\2\2\u06a1\u06a3\5\u02a2\u0152\2\u06a2\u06a1\3\2\2\2\u06a2\u06a3\3\2"+
		"\2\2\u06a3\u06a5\3\2\2\2\u06a4\u06a6\5\u016a\u00b6\2\u06a5\u06a4\3\2\2"+
		"\2\u06a5\u06a6\3\2\2\2\u06a6\u06a8\3\2\2\2\u06a7\u06a9\5\u009aN\2\u06a8"+
		"\u06a7\3\2\2\2\u06a8\u06a9\3\2\2\2\u06a9\u06ab\3\2\2\2\u06aa\u06ac\5\u034a"+
		"\u01a6\2\u06ab\u06aa\3\2\2\2\u06ab\u06ac\3\2\2\2\u06ac\u06ae\3\2\2\2\u06ad"+
		"\u06af\5\u032c\u0197\2\u06ae\u06ad\3\2\2\2\u06ae\u06af\3\2\2\2\u06af\u06b1"+
		"\3\2\2\2\u06b0\u06b2\5\u01fe\u0100\2\u06b1\u06b0\3\2\2\2\u06b1\u06b2\3"+
		"\2\2\2\u06b2\u06b4\3\2\2\2\u06b3\u06b5\5\u00fe\u0080\2\u06b4\u06b3\3\2"+
		"\2\2\u06b4\u06b5\3\2\2\2\u06b5\u06b7\3\2\2\2\u06b6\u06b8\5L\'\2\u06b7"+
		"\u06b6\3\2\2\2\u06b7\u06b8\3\2\2\2\u06b8\u06ba\3\2\2\2\u06b9\u06bb\5\u0258"+
		"\u012d\2\u06ba\u06b9\3\2\2\2\u06ba\u06bb\3\2\2\2\u06bb\u06bd\3\2\2\2\u06bc"+
		"\u06be\5\u0396\u01cc\2\u06bd\u06bc\3\2\2\2\u06bd\u06be\3\2\2\2\u06be\u06c0"+
		"\3\2\2\2\u06bf\u06c1\5\u00ceh\2\u06c0\u06bf\3\2\2\2\u06c0\u06c1\3\2\2"+
		"\2\u06c1\u06c3\3\2\2\2\u06c2\u06c4\5\u01a2\u00d2\2\u06c3\u06c2\3\2\2\2"+
		"\u06c3\u06c4\3\2\2\2\u06c4\u06c6\3\2\2\2\u06c5\u06c7\5\u0282\u0142\2\u06c6"+
		"\u06c5\3\2\2\2\u06c6\u06c7\3\2\2\2\u06c7\u06c9\3\2\2\2\u06c8\u06ca\5\u0254"+
		"\u012b\2\u06c9\u06c8\3\2\2\2\u06c9\u06ca\3\2\2\2\u06ca\u06cc\3\2\2\2\u06cb"+
		"\u06cd\5\u033c\u019f\2\u06cc\u06cb\3\2\2\2\u06cc\u06cd\3\2\2\2\u06cd\u06cf"+
		"\3\2\2\2\u06ce\u06d0\5\u025a\u012e\2\u06cf\u06ce\3\2\2\2\u06cf\u06d0\3"+
		"\2\2\2\u06d0\u06d2\3\2\2\2\u06d1\u06d3\5\u01b8\u00dd\2\u06d2\u06d1\3\2"+
		"\2\2\u06d2\u06d3\3\2\2\2\u06d3\u06d5\3\2\2\2\u06d4\u06d6\58\35\2\u06d5"+
		"\u06d4\3\2\2\2\u06d5\u06d6\3\2\2\2\u06d6\u06d8\3\2\2\2\u06d7\u06d9\5\u0300"+
		"\u0181\2\u06d8\u06d7\3\2\2\2\u06d8\u06d9\3\2\2\2\u06d9\u06db\3\2\2\2\u06da"+
		"\u06dc\5\u0234\u011b\2\u06db\u06da\3\2\2\2\u06db\u06dc\3\2\2\2\u06dc\u06de"+
		"\3\2\2\2\u06dd\u06df\5\u0134\u009b\2\u06de\u06dd\3\2\2\2\u06de\u06df\3"+
		"\2\2\2\u06df\u06e1\3\2\2\2\u06e0\u06e2\5\u01c8\u00e5\2\u06e1\u06e0\3\2"+
		"\2\2\u06e1\u06e2\3\2\2\2\u06e2\u06e4\3\2\2\2\u06e3\u06e5\5\u0298\u014d"+
		"\2\u06e4\u06e3\3\2\2\2\u06e4\u06e5\3\2\2\2\u06e5\u06e7\3\2\2\2\u06e6\u06e8"+
		"\5\u034e\u01a8\2\u06e7\u06e6\3\2\2\2\u06e7\u06e8\3\2\2\2\u06e8\u06ea\3"+
		"\2\2\2\u06e9\u06eb\5\u00ba^\2\u06ea\u06e9\3\2\2\2\u06ea\u06eb\3\2\2\2"+
		"\u06eb\u06ed\3\2\2\2\u06ec\u06ee\5\u032a\u0196\2\u06ed\u06ec\3\2\2\2\u06ed"+
		"\u06ee\3\2\2\2\u06ee\u06f0\3\2\2\2\u06ef\u06f1\5\u015a\u00ae\2\u06f0\u06ef"+
		"\3\2\2\2\u06f0\u06f1\3\2\2\2\u06f1\u06f3\3\2\2\2\u06f2\u06f4\5\u0302\u0182"+
		"\2\u06f3\u06f2\3\2\2\2\u06f3\u06f4\3\2\2\2\u06f4\u06f6\3\2\2\2\u06f5\u06f7"+
		"\5\u0384\u01c3\2\u06f6\u06f5\3\2\2\2\u06f6\u06f7\3\2\2\2\u06f7\u06f9\3"+
		"\2\2\2\u06f8\u06fa\5:\36\2\u06f9\u06f8\3\2\2\2\u06f9\u06fa\3\2\2\2\u06fa"+
		"\u06fc\3\2\2\2\u06fb\u06fd\5\u009eP\2\u06fc\u06fb\3\2\2\2\u06fc\u06fd"+
		"\3\2\2\2\u06fd\u06ff\3\2\2\2\u06fe\u0700\5\u0394\u01cb\2\u06ff\u06fe\3"+
		"\2\2\2\u06ff\u0700\3\2\2\2\u0700\u0702\3\2\2\2\u0701\u0703\5\u0324\u0193"+
		"\2\u0702\u0701\3\2\2\2\u0702\u0703\3\2\2\2\u0703\u0705\3\2\2\2\u0704\u0706"+
		"\5\u01ac\u00d7\2\u0705\u0704\3\2\2\2\u0705\u0706\3\2\2\2\u0706\u0708\3"+
		"\2\2\2\u0707\u0709\5\u017c\u00bf\2\u0708\u0707\3\2\2\2\u0708\u0709\3\2"+
		"\2\2\u0709\u070b\3\2\2\2\u070a\u070c\5\u0368\u01b5\2\u070b\u070a\3\2\2"+
		"\2\u070b\u070c\3\2\2\2\u070c\u0ba9\3\2\2\2\u070d\u070f\7\t\2\2\u070e\u0710"+
		"\5\u017e\u00c0\2\u070f\u070e\3\2\2\2\u070f\u0710\3\2\2\2\u0710\u0712\3"+
		"\2\2\2\u0711\u0713\5\u00e0q\2\u0712\u0711\3\2\2\2\u0712\u0713\3\2\2\2"+
		"\u0713\u0715\3\2\2\2\u0714\u0716\5\u026c\u0137\2\u0715\u0714\3\2\2\2\u0715"+
		"\u0716\3\2\2\2\u0716\u0718\3\2\2\2\u0717\u0719\5\u0128\u0095\2\u0718\u0717"+
		"\3\2\2\2\u0718\u0719\3\2\2\2\u0719\u071b\3\2\2\2\u071a\u071c\5\u0122\u0092"+
		"\2\u071b\u071a\3\2\2\2\u071b\u071c\3\2\2\2\u071c\u071e\3\2\2\2\u071d\u071f"+
		"\5\u0362\u01b2\2\u071e\u071d\3\2\2\2\u071e\u071f\3\2\2\2\u071f\u0720\3"+
		"\2\2\2\u0720\u0721\7\u00b5\2\2\u0721\u0ba9\7\u00b5\2\2\u0722\u0724\7\t"+
		"\2\2\u0723\u0725\5\u017e\u00c0\2\u0724\u0723\3\2\2\2\u0724\u0725\3\2\2"+
		"\2\u0725\u0727\3\2\2\2\u0726\u0728\5\u00e0q\2\u0727\u0726\3\2\2\2\u0727"+
		"\u0728\3\2\2\2\u0728\u072a\3\2\2\2\u0729\u072b\5\u026c\u0137\2\u072a\u0729"+
		"\3\2\2\2\u072a\u072b\3\2\2\2\u072b\u072d\3\2\2\2\u072c\u072e\5\u0128\u0095"+
		"\2\u072d\u072c\3\2\2\2\u072d\u072e\3\2\2\2\u072e\u0730\3\2\2\2\u072f\u0731"+
		"\5\u0122\u0092\2\u0730\u072f\3\2\2\2\u0730\u0731\3\2\2\2\u0731\u0733\3"+
		"\2\2\2\u0732\u0734\5\u0362\u01b2\2\u0733\u0732\3\2\2\2\u0733\u0734\3\2"+
		"\2\2\u0734\u0736\3\2\2\2\u0735\u0737\7\u00b5\2\2\u0736\u0735\3\2\2\2\u0737"+
		"\u0738\3\2\2\2\u0738\u0736\3\2\2\2\u0738\u0739\3\2\2\2\u0739\u073a\3\2"+
		"\2\2\u073a\u0ba9\7\u00b5\2\2\u073b\u073d\7\n\2\2\u073c\u073e\5\u024c\u0127"+
		"\2\u073d\u073c\3\2\2\2\u073d\u073e\3\2\2\2\u073e\u0740\3\2\2\2\u073f\u0741"+
		"\5\u0316\u018c\2\u0740\u073f\3\2\2\2\u0740\u0741\3\2\2\2\u0741\u0743\3"+
		"\2\2\2\u0742\u0744\5J&\2\u0743\u0742\3\2\2\2\u0743\u0744\3\2\2\2\u0744"+
		"\u0746\3\2\2\2\u0745\u0747\5\u0162\u00b2\2\u0746\u0745\3\2\2\2\u0746\u0747"+
		"\3\2\2\2\u0747\u0749\3\2\2\2\u0748\u074a\5\u022a\u0116\2\u0749\u0748\3"+
		"\2\2\2\u0749\u074a\3\2\2\2\u074a\u074c\3\2\2\2\u074b\u074d\5\u0098M\2"+
		"\u074c\u074b\3\2\2\2\u074c\u074d\3\2\2\2\u074d\u074f\3\2\2\2\u074e\u0750"+
		"\5\u031c\u018f\2\u074f\u074e\3\2\2\2\u074f\u0750\3\2\2\2\u0750\u0752\3"+
		"\2\2\2\u0751\u0753\5\u0222\u0112\2\u0752\u0751\3\2\2\2\u0752\u0753\3\2"+
		"\2\2\u0753\u0755\3\2\2\2\u0754\u0756\5\u0158\u00ad\2\u0755\u0754\3\2\2"+
		"\2\u0755\u0756\3\2\2\2\u0756\u0758\3\2\2\2\u0757\u0759\5\u0314\u018b\2"+
		"\u0758\u0757\3\2\2\2\u0758\u0759\3\2\2\2\u0759\u075b\3\2\2\2\u075a\u075c"+
		"\5\u02a4\u0153\2\u075b\u075a\3\2\2\2\u075b\u075c\3\2\2\2\u075c\u075e\3"+
		"\2\2\2\u075d\u075f\5\u00f2z\2\u075e\u075d\3\2\2\2\u075e\u075f\3\2\2\2"+
		"\u075f\u0761\3\2\2\2\u0760\u0762\5(\25\2\u0761\u0760\3\2\2\2\u0761\u0762"+
		"\3\2\2\2\u0762\u0764\3\2\2\2\u0763\u0765\5\u0338\u019d\2\u0764\u0763\3"+
		"\2\2\2\u0764\u0765\3\2\2\2\u0765\u0767\3\2\2\2\u0766\u0768\5\u0174\u00bb"+
		"\2\u0767\u0766\3\2\2\2\u0767\u0768\3\2\2\2\u0768\u076a\3\2\2\2\u0769\u076b"+
		"\5\u016e\u00b8\2\u076a\u0769\3\2\2\2\u076a\u076b\3\2\2\2\u076b\u076d\3"+
		"\2\2\2\u076c\u076e\5\u025e\u0130\2\u076d\u076c\3\2\2\2\u076d\u076e\3\2"+
		"\2\2\u076e\u0770\3\2\2\2\u076f\u0771\5\u0356\u01ac\2\u0770\u076f\3\2\2"+
		"\2\u0770\u0771\3\2\2\2\u0771\u0773\3\2\2\2\u0772\u0774\5\u00e2r\2\u0773"+
		"\u0772\3\2\2\2\u0773\u0774\3\2\2\2\u0774\u0776\3\2\2\2\u0775\u0777\5\u0108"+
		"\u0085\2\u0776\u0775\3\2\2\2\u0776\u0777\3\2\2\2\u0777\u0779\3\2\2\2\u0778"+
		"\u077a\5\u014a\u00a6\2\u0779\u0778\3\2\2\2\u0779\u077a\3\2\2\2\u077a\u077c"+
		"\3\2\2\2\u077b\u077d\5\n\6\2\u077c\u077b\3\2\2\2\u077c\u077d\3\2\2\2\u077d"+
		"\u077f\3\2\2\2\u077e\u0780\5\u02c4\u0163\2\u077f\u077e\3\2\2\2\u077f\u0780"+
		"\3\2\2\2\u0780\u0782\3\2\2\2\u0781\u0783\5\u0288\u0145\2\u0782\u0781\3"+
		"\2\2\2\u0782\u0783\3\2\2\2\u0783\u0785\3\2\2\2\u0784\u0786\5\u0182\u00c2"+
		"\2\u0785\u0784\3\2\2\2\u0785\u0786\3\2\2\2\u0786\u0788\3\2\2\2\u0787\u0789"+
		"\5\u00e6t\2\u0788\u0787\3\2\2\2\u0788\u0789\3\2\2\2\u0789\u078b\3\2\2"+
		"\2\u078a\u078c\5\u0370\u01b9\2\u078b\u078a\3\2\2\2\u078b\u078c\3\2\2\2"+
		"\u078c\u078e\3\2\2\2\u078d\u078f\5\u02de\u0170\2\u078e\u078d\3\2\2\2\u078e"+
		"\u078f\3\2\2\2\u078f\u0791\3\2\2\2\u0790\u0792\5\22\n\2\u0791\u0790\3"+
		"\2\2\2\u0791\u0792\3\2\2\2\u0792\u0794\3\2\2\2\u0793\u0795\5\u015c\u00af"+
		"\2\u0794\u0793\3\2\2\2\u0794\u0795\3\2\2\2\u0795\u0797\3\2\2\2\u0796\u0798"+
		"\5\u02be\u0160\2\u0797\u0796\3\2\2\2\u0797\u0798\3\2\2\2\u0798\u079a\3"+
		"\2\2\2\u0799\u079b\5\u0398\u01cd\2\u079a\u0799\3\2\2\2\u079a\u079b\3\2"+
		"\2\2\u079b\u079d\3\2\2\2\u079c\u079e\5\u029c\u014f\2\u079d\u079c\3\2\2"+
		"\2\u079d\u079e\3\2\2\2\u079e\u07a0\3\2\2\2\u079f\u07a1\5\u01aa\u00d6\2"+
		"\u07a0\u079f\3\2\2\2\u07a0\u07a1\3\2\2\2\u07a1\u07a3\3\2\2\2\u07a2\u07a4"+
		"\5\u0096L\2\u07a3\u07a2\3\2\2\2\u07a3\u07a4\3\2\2\2\u07a4\u07a6\3\2\2"+
		"\2\u07a5\u07a7\5\u02fa\u017e\2\u07a6\u07a5\3\2\2\2\u07a6\u07a7\3\2\2\2"+
		"\u07a7\u07a9\3\2\2\2\u07a8\u07aa\5\u0208\u0105\2\u07a9\u07a8\3\2\2\2\u07a9"+
		"\u07aa\3\2\2\2\u07aa\u07ac\3\2\2\2\u07ab\u07ad\5\u0224\u0113\2\u07ac\u07ab"+
		"\3\2\2\2\u07ac\u07ad\3\2\2\2\u07ad\u07af\3\2\2\2\u07ae\u07b0\5\u0342\u01a2"+
		"\2\u07af\u07ae\3\2\2\2\u07af\u07b0\3\2\2\2\u07b0\u0ba9\3\2\2\2\u07b1\u07b2"+
		"\7\13\2\2\u07b2\u07b4\7\f\2\2\u07b3\u07b5\5\u0186\u00c4\2\u07b4\u07b3"+
		"\3\2\2\2\u07b4\u07b5\3\2\2\2\u07b5\u07b7\3\2\2\2\u07b6\u07b8\5\u0278\u013d"+
		"\2\u07b7\u07b6\3\2\2\2\u07b7\u07b8\3\2\2\2\u07b8\u07ba\3\2\2\2\u07b9\u07bb"+
		"\5f\64\2\u07ba\u07b9\3\2\2\2\u07ba\u07bb\3\2\2\2\u07bb\u07bd\3\2\2\2\u07bc"+
		"\u07be\5\u0188\u00c5\2\u07bd\u07bc\3\2\2\2\u07bd\u07be\3\2\2\2\u07be\u07c0"+
		"\3\2\2\2\u07bf\u07c1\5\u0274\u013b\2\u07c0\u07bf\3\2\2\2\u07c0\u07c1\3"+
		"\2\2\2\u07c1\u07c3\3\2\2\2\u07c2\u07c4\5p9\2\u07c3\u07c2\3\2\2\2\u07c3"+
		"\u07c4\3\2\2\2\u07c4\u07c6\3\2\2\2\u07c5\u07c7\5\u0336\u019c\2\u07c6\u07c5"+
		"\3\2\2\2\u07c6\u07c7\3\2\2\2\u07c7\u07c9\3\2\2\2\u07c8\u07ca\5\u00c0a"+
		"\2\u07c9\u07c8\3\2\2\2\u07c9\u07ca\3\2\2\2\u07ca\u07cc\3\2\2\2\u07cb\u07cd"+
		"\5\u0178\u00bd\2\u07cc\u07cb\3\2\2\2\u07cc\u07cd\3\2\2\2\u07cd\u07cf\3"+
		"\2\2\2\u07ce\u07d0\5\u018c\u00c7\2\u07cf\u07ce\3\2\2\2\u07cf\u07d0\3\2"+
		"\2\2\u07d0\u07d2\3\2\2\2\u07d1\u07d3\5\u0260\u0131\2\u07d2\u07d1\3\2\2"+
		"\2\u07d2\u07d3\3\2\2\2\u07d3\u07d5\3\2\2\2\u07d4\u07d6\5\u012c\u0097\2"+
		"\u07d5\u07d4\3\2\2\2\u07d5\u07d6\3\2\2\2\u07d6\u07d8\3\2\2\2\u07d7\u07d9"+
		"\5\u00d2j\2\u07d8\u07d7\3\2\2\2\u07d8\u07d9\3\2\2\2\u07d9\u07db\3\2\2"+
		"\2\u07da\u07dc\5\u0390\u01c9\2\u07db\u07da\3\2\2\2\u07db\u07dc\3\2\2\2"+
		"\u07dc\u07de\3\2\2\2\u07dd\u07df\5\u0246\u0124\2\u07de\u07dd\3\2\2\2\u07de"+
		"\u07df\3\2\2\2\u07df\u07e1\3\2\2\2\u07e0\u07e2\5\u02f4\u017b\2\u07e1\u07e0"+
		"\3\2\2\2\u07e1\u07e2\3\2\2\2\u07e2\u07e4\3\2\2\2\u07e3\u07e5\5\u02ac\u0157"+
		"\2\u07e4\u07e3\3\2\2\2\u07e4\u07e5\3\2\2\2\u07e5\u07e7\3\2\2\2\u07e6\u07e8"+
		"\5\u00f4{\2\u07e7\u07e6\3\2\2\2\u07e7\u07e8\3\2\2\2\u07e8\u07ea\3\2\2"+
		"\2\u07e9\u07eb\5\u0126\u0094\2\u07ea\u07e9\3\2\2\2\u07ea\u07eb\3\2\2\2"+
		"\u07eb\u07ed\3\2\2\2\u07ec\u07ee\5\u02bc\u015f\2\u07ed\u07ec\3\2\2\2\u07ed"+
		"\u07ee\3\2\2\2\u07ee\u07f0\3\2\2\2\u07ef\u07f1\5\u021c\u010f\2\u07f0\u07ef"+
		"\3\2\2\2\u07f0\u07f1\3\2\2\2\u07f1\u07f3\3\2\2\2\u07f2\u07f4\5~@\2\u07f3"+
		"\u07f2\3\2\2\2\u07f3\u07f4\3\2\2\2\u07f4\u07f6\3\2\2\2\u07f5\u07f7\5\u010a"+
		"\u0086\2\u07f6\u07f5\3\2\2\2\u07f6\u07f7\3\2\2\2\u07f7\u07f9\3\2\2\2\u07f8"+
		"\u07fa\5\u02fc\u017f\2\u07f9\u07f8\3\2\2\2\u07f9\u07fa\3\2\2\2\u07fa\u07fc"+
		"\3\2\2\2\u07fb\u07fd\5<\37\2\u07fc\u07fb\3\2\2\2\u07fc\u07fd\3\2\2\2\u07fd"+
		"\u07ff\3\2\2\2\u07fe\u0800\5\u0226\u0114\2\u07ff\u07fe\3\2\2\2\u07ff\u0800"+
		"\3\2\2\2\u0800\u0802\3\2\2\2\u0801\u0803\5\u0170\u00b9\2\u0802\u0801\3"+
		"\2\2\2\u0802\u0803\3\2\2\2\u0803\u0805\3\2\2\2\u0804\u0806\5\u026e\u0138"+
		"\2\u0805\u0804\3\2\2\2\u0805\u0806\3\2\2\2\u0806\u0808\3\2\2\2\u0807\u0809"+
		"\5\u0374\u01bb\2\u0808\u0807\3\2\2\2\u0808\u0809\3\2\2\2\u0809\u080b\3"+
		"\2\2\2\u080a\u080c\5\u01f4\u00fb\2\u080b\u080a\3\2\2\2\u080b\u080c\3\2"+
		"\2\2\u080c\u080e\3\2\2\2\u080d\u080f\5\u0138\u009d\2\u080e\u080d\3\2\2"+
		"\2\u080e\u080f\3\2\2\2\u080f\u0811\3\2\2\2\u0810\u0812\5\u0238\u011d\2"+
		"\u0811\u0810\3\2\2\2\u0811\u0812\3\2\2\2\u0812\u0814\3\2\2\2\u0813\u0815"+
		"\5\u02c8\u0165\2\u0814\u0813\3\2\2\2\u0814\u0815\3\2\2\2\u0815\u0817\3"+
		"\2\2\2\u0816\u0818\5\u01be\u00e0\2\u0817\u0816\3\2\2\2\u0817\u0818\3\2"+
		"\2\2\u0818\u0ba9\3\2\2\2\u0819\u081a\7\13\2\2\u081a\u081b\7\r\2\2\u081b"+
		"\u081c\7\4\2\2\u081c\u081e\7\u00b5\2\2\u081d\u081f\5\u0186\u00c4\2\u081e"+
		"\u081d\3\2\2\2\u081e\u081f\3\2\2\2\u081f\u0821\3\2\2\2\u0820\u0822\5\u0278"+
		"\u013d\2\u0821\u0820\3\2\2\2\u0821\u0822\3\2\2\2\u0822\u0824\3\2\2\2\u0823"+
		"\u0825\5f\64\2\u0824\u0823\3\2\2\2\u0824\u0825\3\2\2\2\u0825\u0827\3\2"+
		"\2\2\u0826\u0828\5\u0188\u00c5\2\u0827\u0826\3\2\2\2\u0827\u0828\3\2\2"+
		"\2\u0828\u082a\3\2\2\2\u0829\u082b\5\u0274\u013b\2\u082a\u0829\3\2\2\2"+
		"\u082a\u082b\3\2\2\2\u082b\u082d\3\2\2\2\u082c\u082e\5p9\2\u082d\u082c"+
		"\3\2\2\2\u082d\u082e\3\2\2\2\u082e\u0830\3\2\2\2\u082f\u0831\5\u0336\u019c"+
		"\2\u0830\u082f\3\2\2\2\u0830\u0831\3\2\2\2\u0831\u0833\3\2\2\2\u0832\u0834"+
		"\5\u00c0a\2\u0833\u0832\3\2\2\2\u0833\u0834\3\2\2\2\u0834\u0836\3\2\2"+
		"\2\u0835\u0837\5\u0178\u00bd\2\u0836\u0835\3\2\2\2\u0836\u0837\3\2\2\2"+
		"\u0837\u0839\3\2";
	private static final String _serializedATNSegment1 =
		"\2\2\u0838\u083a\5\u018c\u00c7\2\u0839\u0838\3\2\2\2\u0839\u083a\3\2\2"+
		"\2\u083a\u083c\3\2\2\2\u083b\u083d\5\u012c\u0097\2\u083c\u083b\3\2\2\2"+
		"\u083c\u083d\3\2\2\2\u083d\u083f\3\2\2\2\u083e\u0840\5\u00d2j\2\u083f"+
		"\u083e\3\2\2\2\u083f\u0840\3\2\2\2\u0840\u0842\3\2\2\2\u0841\u0843\5\u0390"+
		"\u01c9\2\u0842\u0841\3\2\2\2\u0842\u0843\3\2\2\2\u0843\u0845\3\2\2\2\u0844"+
		"\u0846\5\u0246\u0124\2\u0845\u0844\3\2\2\2\u0845\u0846\3\2\2\2\u0846\u0848"+
		"\3\2\2\2\u0847\u0849\5\u02f4\u017b\2\u0848\u0847\3\2\2\2\u0848\u0849\3"+
		"\2\2\2\u0849\u084b\3\2\2\2\u084a\u084c\5\u02ac\u0157\2\u084b\u084a\3\2"+
		"\2\2\u084b\u084c\3\2\2\2\u084c\u084e\3\2\2\2\u084d\u084f\5\u00f4{\2\u084e"+
		"\u084d\3\2\2\2\u084e\u084f\3\2\2\2\u084f\u0851\3\2\2\2\u0850\u0852\5\u0126"+
		"\u0094\2\u0851\u0850\3\2\2\2\u0851\u0852\3\2\2\2\u0852\u0854\3\2\2\2\u0853"+
		"\u0855\5\u02bc\u015f\2\u0854\u0853\3\2\2\2\u0854\u0855\3\2\2\2\u0855\u0857"+
		"\3\2\2\2\u0856\u0858\5\u021c\u010f\2\u0857\u0856\3\2\2\2\u0857\u0858\3"+
		"\2\2\2\u0858\u085a\3\2\2\2\u0859\u085b\5~@\2\u085a\u0859\3\2\2\2\u085a"+
		"\u085b\3\2\2\2\u085b\u085d\3\2\2\2\u085c\u085e\5\u010a\u0086\2\u085d\u085c"+
		"\3\2\2\2\u085d\u085e\3\2\2\2\u085e\u0860\3\2\2\2\u085f\u0861\5\u02fc\u017f"+
		"\2\u0860\u085f\3\2\2\2\u0860\u0861\3\2\2\2\u0861\u0863\3\2\2\2\u0862\u0864"+
		"\5<\37\2\u0863\u0862\3\2\2\2\u0863\u0864\3\2\2\2\u0864\u0866\3\2\2\2\u0865"+
		"\u0867\5\u0226\u0114\2\u0866\u0865\3\2\2\2\u0866\u0867\3\2\2\2\u0867\u0869"+
		"\3\2\2\2\u0868\u086a\5\u0170\u00b9\2\u0869\u0868\3\2\2\2\u0869\u086a\3"+
		"\2\2\2\u086a\u086c\3\2\2\2\u086b\u086d\5\u026e\u0138\2\u086c\u086b\3\2"+
		"\2\2\u086c\u086d\3\2\2\2\u086d\u086f\3\2\2\2\u086e\u0870\5\u0374\u01bb"+
		"\2\u086f\u086e\3\2\2\2\u086f\u0870\3\2\2\2\u0870\u0872\3\2\2\2\u0871\u0873"+
		"\5\u01f4\u00fb\2\u0872\u0871\3\2\2\2\u0872\u0873\3\2\2\2\u0873\u0875\3"+
		"\2\2\2\u0874\u0876\5\u01be\u00e0\2\u0875\u0874\3\2\2\2\u0875\u0876\3\2"+
		"\2\2\u0876\u0ba9\3\2\2\2\u0877\u0878\7\13\2\2\u0878\u0879\7\16\2\2\u0879"+
		"\u087a\7\4\2\2\u087a\u087c\7\u00b5\2\2\u087b\u087d\5\u0186\u00c4\2\u087c"+
		"\u087b\3\2\2\2\u087c\u087d\3\2\2\2\u087d\u087f\3\2\2\2\u087e\u0880\5\u0278"+
		"\u013d\2\u087f\u087e\3\2\2\2\u087f\u0880\3\2\2\2\u0880\u0882\3\2\2\2\u0881"+
		"\u0883\5\u0188\u00c5\2\u0882\u0881\3\2\2\2\u0882\u0883\3\2\2\2\u0883\u0885"+
		"\3\2\2\2\u0884\u0886\5\u0256\u012c\2\u0885\u0884\3\2\2\2\u0885\u0886\3"+
		"\2\2\2\u0886\u0888\3\2\2\2\u0887\u0889\5p9\2\u0888\u0887\3\2\2\2\u0888"+
		"\u0889\3\2\2\2\u0889\u088b\3\2\2\2\u088a\u088c\5\u0178\u00bd\2\u088b\u088a"+
		"\3\2\2\2\u088b\u088c\3\2\2\2\u088c\u088e\3\2\2\2\u088d\u088f\5\u018c\u00c7"+
		"\2\u088e\u088d\3\2\2\2\u088e\u088f\3\2\2\2\u088f\u0891\3\2\2\2\u0890\u0892"+
		"\5\u00d2j\2\u0891\u0890\3\2\2\2\u0891\u0892\3\2\2\2\u0892\u0894\3\2\2"+
		"\2\u0893\u0895\5\u0390\u01c9\2\u0894\u0893\3\2\2\2\u0894\u0895\3\2\2\2"+
		"\u0895\u0897\3\2\2\2\u0896\u0898\5\u0246\u0124\2\u0897\u0896\3\2\2\2\u0897"+
		"\u0898\3\2\2\2\u0898\u089a\3\2\2\2\u0899\u089b\5\u02f4\u017b\2\u089a\u0899"+
		"\3\2\2\2\u089a\u089b\3\2\2\2\u089b\u089d\3\2\2\2\u089c\u089e\5\u02ac\u0157"+
		"\2\u089d\u089c\3\2\2\2\u089d\u089e\3\2\2\2\u089e\u08a0\3\2\2\2\u089f\u08a1"+
		"\5\u00f4{\2\u08a0\u089f\3\2\2\2\u08a0\u08a1\3\2\2\2\u08a1\u08a3\3\2\2"+
		"\2\u08a2\u08a4\5\u02bc\u015f\2\u08a3\u08a2\3\2\2\2\u08a3\u08a4\3\2\2\2"+
		"\u08a4\u08a6\3\2\2\2\u08a5\u08a7\5\u021c\u010f\2\u08a6\u08a5\3\2\2\2\u08a6"+
		"\u08a7\3\2\2\2\u08a7\u08a9\3\2\2\2\u08a8\u08aa\5~@\2\u08a9\u08a8\3\2\2"+
		"\2\u08a9\u08aa\3\2\2\2\u08aa\u08ac\3\2\2\2\u08ab\u08ad\5\u010a\u0086\2"+
		"\u08ac\u08ab\3\2\2\2\u08ac\u08ad\3\2\2\2\u08ad\u08af\3\2\2\2\u08ae\u08b0"+
		"\5\u02fc\u017f\2\u08af\u08ae\3\2\2\2\u08af\u08b0\3\2\2\2\u08b0\u08b2\3"+
		"\2\2\2\u08b1\u08b3\5<\37\2\u08b2\u08b1\3\2\2\2\u08b2\u08b3\3\2\2\2\u08b3"+
		"\u08b5\3\2\2\2\u08b4\u08b6\5\u0226\u0114\2\u08b5\u08b4\3\2\2\2\u08b5\u08b6"+
		"\3\2\2\2\u08b6\u08b8\3\2\2\2\u08b7\u08b9\5\u0170\u00b9\2\u08b8\u08b7\3"+
		"\2\2\2\u08b8\u08b9\3\2\2\2\u08b9\u08bb\3\2\2\2\u08ba\u08bc\5\u026e\u0138"+
		"\2\u08bb\u08ba\3\2\2\2\u08bb\u08bc\3\2\2\2\u08bc\u08be\3\2\2\2\u08bd\u08bf"+
		"\5\u0374\u01bb\2\u08be\u08bd\3\2\2\2\u08be\u08bf\3\2\2\2\u08bf\u08c1\3"+
		"\2\2\2\u08c0\u08c2\5\u01f4\u00fb\2\u08c1\u08c0\3\2\2\2\u08c1\u08c2\3\2"+
		"\2\2\u08c2\u08c4\3\2\2\2\u08c3\u08c5\5\u01be\u00e0\2\u08c4\u08c3\3\2\2"+
		"\2\u08c4\u08c5\3\2\2\2\u08c5\u0ba9\3\2\2\2\u08c6\u08c7\7\13\2\2\u08c7"+
		"\u08c9\7\17\2\2\u08c8\u08ca\5\u0186\u00c4\2\u08c9\u08c8\3\2\2\2\u08c9"+
		"\u08ca\3\2\2\2\u08ca\u08cc\3\2\2\2\u08cb\u08cd\5\u0278\u013d\2\u08cc\u08cb"+
		"\3\2\2\2\u08cc\u08cd\3\2\2\2\u08cd\u08cf\3\2\2\2\u08ce\u08d0\5\u0188\u00c5"+
		"\2\u08cf\u08ce\3\2\2\2\u08cf\u08d0\3\2\2\2\u08d0\u08d2\3\2\2\2\u08d1\u08d3"+
		"\5p9\2\u08d2\u08d1\3\2\2\2\u08d2\u08d3\3\2\2\2\u08d3\u08d5\3\2\2\2\u08d4"+
		"\u08d6\5\u0178\u00bd\2\u08d5\u08d4\3\2\2\2\u08d5\u08d6\3\2\2\2\u08d6\u08d8"+
		"\3\2\2\2\u08d7\u08d9\5\u018c\u00c7\2\u08d8\u08d7\3\2\2\2\u08d8\u08d9\3"+
		"\2\2\2\u08d9\u08db\3\2\2\2\u08da\u08dc\5\u00d2j\2\u08db\u08da\3\2\2\2"+
		"\u08db\u08dc\3\2\2\2\u08dc\u08de\3\2\2\2\u08dd\u08df\5\u01a4\u00d3\2\u08de"+
		"\u08dd\3\2\2\2\u08de\u08df\3\2\2\2\u08df\u08e1\3\2\2\2\u08e0\u08e2\5~"+
		"@\2\u08e1\u08e0\3\2\2\2\u08e1\u08e2\3\2\2\2\u08e2\u08e4\3\2\2\2\u08e3"+
		"\u08e5\5\u010a\u0086\2\u08e4\u08e3\3\2\2\2\u08e4\u08e5\3\2\2\2\u08e5\u08e7"+
		"\3\2\2\2\u08e6\u08e8\5N(\2\u08e7\u08e6\3\2\2\2\u08e7\u08e8\3\2\2\2\u08e8"+
		"\u08ea\3\2\2\2\u08e9\u08eb\5\u02fc\u017f\2\u08ea\u08e9\3\2\2\2\u08ea\u08eb"+
		"\3\2\2\2\u08eb\u08ed\3\2\2\2\u08ec\u08ee\5<\37\2\u08ed\u08ec\3\2\2\2\u08ed"+
		"\u08ee\3\2\2\2\u08ee\u08f0\3\2\2\2\u08ef\u08f1\5\u0226\u0114\2\u08f0\u08ef"+
		"\3\2\2\2\u08f0\u08f1\3\2\2\2\u08f1\u08f3\3\2\2\2\u08f2\u08f4\5\u0170\u00b9"+
		"\2\u08f3\u08f2\3\2\2\2\u08f3\u08f4\3\2\2\2\u08f4\u08f6\3\2\2\2\u08f5\u08f7"+
		"\5\u026e\u0138\2\u08f6\u08f5\3\2\2\2\u08f6\u08f7\3\2\2\2\u08f7\u08f9\3"+
		"\2\2\2\u08f8\u08fa\5\u0374\u01bb\2\u08f9\u08f8\3\2\2\2\u08f9\u08fa\3\2"+
		"\2\2\u08fa\u08fc\3\2\2\2\u08fb\u08fd\5\u01f4\u00fb\2\u08fc\u08fb\3\2\2"+
		"\2\u08fc\u08fd\3\2\2\2\u08fd\u08ff\3\2\2\2\u08fe\u0900\5\u017a\u00be\2"+
		"\u08ff\u08fe\3\2\2\2\u08ff\u0900\3\2\2\2\u0900\u0ba9\3\2\2\2\u0901\u0902"+
		"\7\13\2\2\u0902\u0904\7\20\2\2\u0903\u0905\5\u0186\u00c4\2\u0904\u0903"+
		"\3\2\2\2\u0904\u0905\3\2\2\2\u0905\u0907\3\2\2\2\u0906\u0908\5\u0278\u013d"+
		"\2\u0907\u0906\3\2\2\2\u0907\u0908\3\2\2\2\u0908\u090a\3\2\2\2\u0909\u090b"+
		"\5\u0212\u010a\2\u090a\u0909\3\2\2\2\u090a\u090b\3\2\2\2\u090b\u090d\3"+
		"\2\2\2\u090c\u090e\5\u0188\u00c5\2\u090d\u090c\3\2\2\2\u090d\u090e\3\2"+
		"\2\2\u090e\u0910\3\2\2\2\u090f\u0911\5p9\2\u0910\u090f\3\2\2\2\u0910\u0911"+
		"\3\2\2\2\u0911\u0913\3\2\2\2\u0912\u0914\5\u0178\u00bd\2\u0913\u0912\3"+
		"\2\2\2\u0913\u0914\3\2\2\2\u0914\u0916\3\2\2\2\u0915\u0917\5\u018c\u00c7"+
		"\2\u0916\u0915\3\2\2\2\u0916\u0917\3\2\2\2\u0917\u0919\3\2\2\2\u0918\u091a"+
		"\5\u0360\u01b1\2\u0919\u0918\3\2\2\2\u0919\u091a\3\2\2\2\u091a\u091c\3"+
		"\2\2\2\u091b\u091d\5\u011e\u0090\2\u091c\u091b\3\2\2\2\u091c\u091d\3\2"+
		"\2\2\u091d\u091f\3\2\2\2\u091e\u0920\5\u00d2j\2\u091f\u091e\3\2\2\2\u091f"+
		"\u0920\3\2\2\2\u0920\u0922\3\2\2\2\u0921\u0923\5\u00fa~\2\u0922\u0921"+
		"\3\2\2\2\u0922\u0923\3\2\2\2\u0923\u0925\3\2\2\2\u0924\u0926\5\u00aeX"+
		"\2\u0925\u0924\3\2\2\2\u0925\u0926\3\2\2\2\u0926\u0928\3\2\2\2\u0927\u0929"+
		"\5\u01a4\u00d3\2\u0928\u0927\3\2\2\2\u0928\u0929\3\2\2\2\u0929\u092b\3"+
		"\2\2\2\u092a\u092c\5\u02bc\u015f\2\u092b\u092a\3\2\2\2\u092b\u092c\3\2"+
		"\2\2\u092c\u092e\3\2\2\2\u092d\u092f\5~@\2\u092e\u092d\3\2\2\2\u092e\u092f"+
		"\3\2\2\2\u092f\u0931\3\2\2\2\u0930\u0932\5\u010a\u0086\2\u0931\u0930\3"+
		"\2\2\2\u0931\u0932\3\2\2\2\u0932\u0934\3\2\2\2\u0933\u0935\5\u02e8\u0175"+
		"\2\u0934\u0933\3\2\2\2\u0934\u0935\3\2\2\2\u0935\u0937\3\2\2\2\u0936\u0938"+
		"\5N(\2\u0937\u0936\3\2\2\2\u0937\u0938\3\2\2\2\u0938\u093a\3\2\2\2\u0939"+
		"\u093b\5\u00b2Z\2\u093a\u0939\3\2\2\2\u093a\u093b\3\2\2\2\u093b\u093d"+
		"\3\2\2\2\u093c\u093e\5\4\3\2\u093d\u093c\3\2\2\2\u093d\u093e\3\2\2\2\u093e"+
		"\u0940\3\2\2\2\u093f\u0941\5\u02fc\u017f\2\u0940\u093f\3\2\2\2\u0940\u0941"+
		"\3\2\2\2\u0941\u0943\3\2\2\2\u0942\u0944\5<\37\2\u0943\u0942\3\2\2\2\u0943"+
		"\u0944\3\2\2\2\u0944\u0946\3\2\2\2\u0945\u0947\5\u015e\u00b0\2\u0946\u0945"+
		"\3\2\2\2\u0946\u0947\3\2\2\2\u0947\u0949\3\2\2\2\u0948\u094a\5\u0226\u0114"+
		"\2\u0949\u0948\3\2\2\2\u0949\u094a\3\2\2\2\u094a\u094c\3\2\2\2\u094b\u094d"+
		"\5\u0170\u00b9\2\u094c\u094b\3\2\2\2\u094c\u094d\3\2\2\2\u094d\u094f\3"+
		"\2\2\2\u094e\u0950\5\u026e\u0138\2\u094f\u094e\3\2\2\2\u094f\u0950\3\2"+
		"\2\2\u0950\u0952\3\2\2\2\u0951\u0953\5\u0374\u01bb\2\u0952\u0951\3\2\2"+
		"\2\u0952\u0953\3\2\2\2\u0953\u0955\3\2\2\2\u0954\u0956\5\u01f4\u00fb\2"+
		"\u0955\u0954\3\2\2\2\u0955\u0956\3\2\2\2\u0956\u0958\3\2\2\2\u0957\u0959"+
		"\5\u017a\u00be\2\u0958\u0957\3\2\2\2\u0958\u0959\3\2\2\2\u0959\u0ba9\3"+
		"\2\2\2\u095a\u095c\7\21\2\2\u095b\u095d\5\u0204\u0103\2\u095c\u095b\3"+
		"\2\2\2\u095c\u095d\3\2\2\2\u095d\u095f\3\2\2\2\u095e\u0960\5\u029a\u014e"+
		"\2\u095f\u095e\3\2\2\2\u095f\u0960\3\2\2\2\u0960\u0962\3\2\2\2\u0961\u0963"+
		"\5\u01cc\u00e7\2\u0962\u0961\3\2\2\2\u0962\u0963\3\2\2\2\u0963\u0965\3"+
		"\2\2\2\u0964\u0966\5\u027a\u013e\2\u0965\u0964\3\2\2\2\u0965\u0966\3\2"+
		"\2\2\u0966\u0968\3\2\2\2\u0967\u0969\5\u02ee\u0178\2\u0968\u0967\3\2\2"+
		"\2\u0968\u0969\3\2\2\2\u0969\u096b\3\2\2\2\u096a\u096c\5\u00eex\2\u096b"+
		"\u096a\3\2\2\2\u096b\u096c\3\2\2\2\u096c\u096e\3\2\2\2\u096d\u096f\5\u02f0"+
		"\u0179\2\u096e\u096d\3\2\2\2\u096e\u096f\3\2\2\2\u096f\u0971\3\2\2\2\u0970"+
		"\u0972\5\u0332\u019a\2\u0971\u0970\3\2\2\2\u0971\u0972\3\2\2\2\u0972\u0974"+
		"\3\2\2\2\u0973\u0975\5\34\17\2\u0974\u0973\3\2\2\2\u0974\u0975\3\2\2\2"+
		"\u0975\u0977\3\2\2\2\u0976\u0978\5d\63\2\u0977\u0976\3\2\2\2\u0977\u0978"+
		"\3\2\2\2\u0978\u097a\3\2\2\2\u0979\u097b\5r:\2\u097a\u0979\3\2\2\2\u097a"+
		"\u097b\3\2\2\2\u097b\u097d\3\2\2\2\u097c\u097e\5\u038c\u01c7\2\u097d\u097c"+
		"\3\2\2\2\u097d\u097e\3\2\2\2\u097e\u0ba9\3\2\2\2\u097f\u0981\7\22\2\2"+
		"\u0980\u0982\5\u00b0Y\2\u0981\u0980\3\2\2\2\u0981\u0982\3\2\2\2\u0982"+
		"\u0984\3\2\2\2\u0983\u0985\5\u0112\u008a\2\u0984\u0983\3\2\2\2\u0984\u0985"+
		"\3\2\2\2\u0985\u0987\3\2\2\2\u0986\u0988\5\u0080A\2\u0987\u0986\3\2\2"+
		"\2\u0987\u0988\3\2\2\2\u0988\u098a\3\2\2\2\u0989\u098b\5\u02ec\u0177\2"+
		"\u098a\u0989\3\2\2\2\u098a\u098b\3\2\2\2\u098b\u098c\3\2\2\2\u098c\u098e"+
		"\7\u00b5\2\2\u098d\u098f\5\u031e\u0190\2\u098e\u098d\3\2\2\2\u098e\u098f"+
		"\3\2\2\2\u098f\u0ba9\3\2\2\2\u0990\u0992\7\22\2\2\u0991\u0993\5\u00b0"+
		"Y\2\u0992\u0991\3\2\2\2\u0992\u0993\3\2\2\2\u0993\u0995\3\2\2\2\u0994"+
		"\u0996\5\u0112\u008a\2\u0995\u0994\3\2\2\2\u0995\u0996\3\2\2\2\u0996\u0998"+
		"\3\2\2\2\u0997\u0999\5\u0080A\2\u0998\u0997\3\2\2\2\u0998\u0999\3\2\2"+
		"\2\u0999\u099b\3\2\2\2\u099a\u099c\5\u02ec\u0177\2\u099b\u099a\3\2\2\2"+
		"\u099b\u099c\3\2\2\2\u099c\u099e\3\2\2\2\u099d\u099f\5\u0252\u012a\2\u099e"+
		"\u099d\3\2\2\2\u099e\u099f\3\2\2\2\u099f\u09a1\3\2\2\2\u09a0\u09a2\5\u00ac"+
		"W\2\u09a1\u09a0\3\2\2\2\u09a1\u09a2\3\2\2\2\u09a2\u09a4\3\2\2\2\u09a3"+
		"\u09a5\5\u01ea\u00f6\2\u09a4\u09a3\3\2\2\2\u09a4\u09a5\3\2\2\2\u09a5\u09a7"+
		"\3\2\2\2\u09a6\u09a8\5\u031e\u0190\2\u09a7\u09a6\3\2\2\2\u09a7\u09a8\3"+
		"\2\2\2\u09a8\u0ba9\3\2\2\2\u09a9\u09ab\7\23\2\2\u09aa\u09ac\5\u00c8e\2"+
		"\u09ab\u09aa\3\2\2\2\u09ab\u09ac\3\2\2\2\u09ac\u09ae\3\2\2\2\u09ad\u09af"+
		"\5\u0206\u0104\2\u09ae\u09ad\3\2\2\2\u09ae\u09af\3\2\2\2\u09af\u09b1\3"+
		"\2\2\2\u09b0\u09b2\5\u0228\u0115\2\u09b1\u09b0\3\2\2\2\u09b1\u09b2\3\2"+
		"\2\2\u09b2\u09b4\3\2\2\2\u09b3\u09b5\5\u0304\u0183\2\u09b4\u09b3\3\2\2"+
		"\2\u09b4\u09b5\3\2\2\2\u09b5\u0ba9\3\2\2\2\u09b6\u09b8\7\24\2\2\u09b7"+
		"\u09b9\5H%\2\u09b8\u09b7\3\2\2\2\u09b8\u09b9\3\2\2\2\u09b9\u09bb\3\2\2"+
		"\2\u09ba\u09bc\5\u02ba\u015e\2\u09bb\u09ba\3\2\2\2\u09bb\u09bc\3\2\2\2"+
		"\u09bc\u09be\3\2\2\2\u09bd\u09bf\5\u0216\u010c\2\u09be\u09bd\3\2\2\2\u09be"+
		"\u09bf\3\2\2\2\u09bf\u09c1\3\2\2\2\u09c0\u09c2\5@!\2\u09c1\u09c0\3\2\2"+
		"\2\u09c1\u09c2\3\2\2\2\u09c2\u09c4\3\2\2\2\u09c3\u09c5\5\u0244\u0123\2"+
		"\u09c4\u09c3\3\2\2\2\u09c4\u09c5\3\2\2\2\u09c5\u09c7\3\2\2\2\u09c6\u09c8"+
		"\5\u037c\u01bf\2\u09c7\u09c6\3\2\2\2\u09c7\u09c8\3\2\2\2\u09c8\u09ca\3"+
		"\2\2\2\u09c9\u09cb\5\60\31\2\u09ca\u09c9\3\2\2\2\u09ca\u09cb\3\2\2\2\u09cb"+
		"\u09cd\3\2\2\2\u09cc\u09ce\5\u011a\u008e\2\u09cd\u09cc\3\2\2\2\u09cd\u09ce"+
		"\3\2\2\2\u09ce\u09d0\3\2\2\2\u09cf\u09d1\7\u00b5\2\2\u09d0\u09cf\3\2\2"+
		"\2\u09d1\u09d2\3\2\2\2\u09d2\u09d0\3\2\2\2\u09d2\u09d3\3\2\2\2\u09d3\u0ba9"+
		"\3\2\2\2\u09d4\u09d6\7\25\2\2\u09d5\u09d7\5\u0320\u0191\2\u09d6\u09d5"+
		"\3\2\2\2\u09d6\u09d7\3\2\2\2\u09d7\u09d9\3\2\2\2\u09d8\u09da\5\u0242\u0122"+
		"\2\u09d9\u09d8\3\2\2\2\u09d9\u09da\3\2\2\2\u09da\u0ba9\3\2\2\2\u09db\u09dd"+
		"\7\26\2\2\u09dc\u09de\5\u028a\u0146\2\u09dd\u09dc\3\2\2\2\u09dd\u09de"+
		"\3\2\2\2\u09de\u09e0\3\2\2\2\u09df\u09e1\5\u0124\u0093\2\u09e0\u09df\3"+
		"\2\2\2\u09e0\u09e1\3\2\2\2\u09e1\u09e3\3\2\2\2\u09e2\u09e4\5\u01e4\u00f3"+
		"\2\u09e3\u09e2\3\2\2\2\u09e3\u09e4\3\2\2\2\u09e4\u09e6\3\2\2\2\u09e5\u09e7"+
		"\5j\66\2\u09e6\u09e5\3\2\2\2\u09e6\u09e7\3\2\2\2\u09e7\u09e9\3\2\2\2\u09e8"+
		"\u09ea\5\u014c\u00a7\2\u09e9\u09e8\3\2\2\2\u09e9\u09ea\3\2\2\2\u09ea\u0ba9"+
		"\3\2\2\2\u09eb\u09ed\7\27\2\2\u09ec\u09ee\5\u012e\u0098\2\u09ed\u09ec"+
		"\3\2\2\2\u09ed\u09ee\3\2\2\2\u09ee\u09f0\3\2\2\2\u09ef\u09f1\5*\26\2\u09f0"+
		"\u09ef\3\2\2\2\u09f0\u09f1\3\2\2\2\u09f1\u09f3\3\2\2\2\u09f2\u09f4\5\u00a4"+
		"S\2\u09f3\u09f2\3\2\2\2\u09f3\u09f4\3\2\2\2\u09f4\u09f5\3\2\2\2\u09f5"+
		"\u09f7\7\u00b5\2\2\u09f6\u09f8\7\u00b5\2\2\u09f7\u09f6\3\2\2\2\u09f8\u09f9"+
		"\3\2\2\2\u09f9\u09f7\3\2\2\2\u09f9\u09fa\3\2\2\2\u09fa\u0ba9\3\2\2\2\u09fb"+
		"\u09fd\7\27\2\2\u09fc\u09fe\5\u012e\u0098\2\u09fd\u09fc\3\2\2\2\u09fd"+
		"\u09fe\3\2\2\2\u09fe\u0a00\3\2\2\2\u09ff\u0a01\5*\26\2\u0a00\u09ff\3\2"+
		"\2\2\u0a00\u0a01\3\2\2\2\u0a01\u0a03\3\2\2\2\u0a02\u0a04\5\u00a4S\2\u0a03"+
		"\u0a02\3\2\2\2\u0a03\u0a04\3\2\2\2\u0a04\u0a06\3\2\2\2\u0a05\u0a07\5\u0154"+
		"\u00ab\2\u0a06\u0a05\3\2\2\2\u0a06\u0a07\3\2\2\2\u0a07\u0a08\3\2\2\2\u0a08"+
		"\u0a0a\7\30\2\2\u0a09\u0a0b\7\u00b5\2\2\u0a0a\u0a09\3\2\2\2\u0a0b\u0a0c"+
		"\3\2\2\2\u0a0c\u0a0a\3\2\2\2\u0a0c\u0a0d\3\2\2\2\u0a0d\u0ba9\3\2\2\2\u0a0e"+
		"\u0a10\7\27\2\2\u0a0f\u0a11\5\u012e\u0098\2\u0a10\u0a0f\3\2\2\2\u0a10"+
		"\u0a11\3\2\2\2\u0a11\u0a13\3\2\2\2\u0a12\u0a14\5\u027e\u0140\2\u0a13\u0a12"+
		"\3\2\2\2\u0a13\u0a14\3\2\2\2\u0a14\u0a16\3\2\2\2\u0a15\u0a17\5*\26\2\u0a16"+
		"\u0a15\3\2\2\2\u0a16\u0a17\3\2\2\2\u0a17\u0a19\3\2\2\2\u0a18\u0a1a\5\u00a4"+
		"S\2\u0a19\u0a18\3\2\2\2\u0a19\u0a1a\3\2\2\2\u0a1a\u0a1c\3\2\2\2\u0a1b"+
		"\u0a1d\5\u01f8\u00fd\2\u0a1c\u0a1b\3\2\2\2\u0a1c\u0a1d\3\2\2\2\u0a1d\u0a1f"+
		"\3\2\2\2\u0a1e\u0a20\7\u00b5\2\2\u0a1f\u0a1e\3\2\2\2\u0a20\u0a21\3\2\2"+
		"\2\u0a21\u0a1f\3\2\2\2\u0a21\u0a22\3\2\2\2\u0a22\u0ba9\3\2\2\2\u0a23\u0a25"+
		"\7\27\2\2\u0a24\u0a26\5\u012e\u0098\2\u0a25\u0a24\3\2\2\2\u0a25\u0a26"+
		"\3\2\2\2\u0a26\u0a28\3\2\2\2\u0a27\u0a29\5\u027e\u0140\2\u0a28\u0a27\3"+
		"\2\2\2\u0a28\u0a29\3\2\2\2\u0a29\u0a2b\3\2\2\2\u0a2a\u0a2c\5*\26\2\u0a2b"+
		"\u0a2a\3\2\2\2\u0a2b\u0a2c\3\2\2\2\u0a2c\u0a2e\3\2\2\2\u0a2d\u0a2f\5\u00a4"+
		"S\2\u0a2e\u0a2d\3\2\2\2\u0a2e\u0a2f\3\2\2\2\u0a2f\u0a31\3\2\2\2\u0a30"+
		"\u0a32\5\u034c\u01a7\2\u0a31\u0a30\3\2\2\2\u0a31\u0a32\3\2\2\2\u0a32\u0a34"+
		"\3\2\2\2\u0a33\u0a35\7\u00b5\2\2\u0a34\u0a33\3\2\2\2\u0a35\u0a36\3\2\2"+
		"\2\u0a36\u0a34\3\2\2\2\u0a36\u0a37\3\2\2\2\u0a37\u0ba9\3\2\2\2\u0a38\u0a3a"+
		"\7\27\2\2\u0a39\u0a3b\5\u012e\u0098\2\u0a3a\u0a39\3\2\2\2\u0a3a\u0a3b"+
		"\3\2\2\2\u0a3b\u0a3d\3\2\2\2\u0a3c\u0a3e\5\u027e\u0140\2\u0a3d\u0a3c\3"+
		"\2\2\2\u0a3d\u0a3e\3\2\2\2\u0a3e\u0a40\3\2\2\2\u0a3f\u0a41\5*\26\2\u0a40"+
		"\u0a3f\3\2\2\2\u0a40\u0a41\3\2\2\2\u0a41\u0a43\3\2\2\2\u0a42\u0a44\5\u00a4"+
		"S\2\u0a43\u0a42\3\2\2\2\u0a43\u0a44\3\2\2\2\u0a44\u0a46\3\2\2\2\u0a45"+
		"\u0a47\5\u0100\u0081\2\u0a46\u0a45\3\2\2\2\u0a46\u0a47\3\2\2\2\u0a47\u0a49"+
		"\3\2\2\2\u0a48\u0a4a\7\u00b5\2\2\u0a49\u0a48\3\2\2\2\u0a4a\u0a4b\3\2\2"+
		"\2\u0a4b\u0a49\3\2\2\2\u0a4b\u0a4c\3\2\2\2\u0a4c\u0ba9\3\2\2\2\u0a4d\u0a4f"+
		"\7\31\2\2\u0a4e\u0a50\5\u0344\u01a3\2\u0a4f\u0a4e\3\2\2\2\u0a4f\u0a50"+
		"\3\2\2\2\u0a50\u0a52\3\2\2\2\u0a51\u0a53\5\u0270\u0139\2\u0a52\u0a51\3"+
		"\2\2\2\u0a52\u0a53\3\2\2\2\u0a53\u0a55\3\2\2\2\u0a54\u0a56\5\u032e\u0198"+
		"\2\u0a55\u0a54\3\2\2\2\u0a55\u0a56\3\2\2\2\u0a56\u0a58\3\2\2\2\u0a57\u0a59"+
		"\5\u0376\u01bc\2\u0a58\u0a57\3\2\2\2\u0a58\u0a59\3\2\2\2\u0a59\u0a5a\3"+
		"\2\2\2\u0a5a\u0a5c\7\u00b5\2\2\u0a5b\u0a5d\7\u00b5\2\2\u0a5c\u0a5b\3\2"+
		"\2\2\u0a5d\u0a5e\3\2\2\2\u0a5e\u0a5c\3\2\2\2\u0a5e\u0a5f\3\2\2\2\u0a5f"+
		"\u0ba9\3\2\2\2\u0a60\u0a62\7\32\2\2\u0a61\u0a63\5\u0248\u0125\2\u0a62"+
		"\u0a61\3\2\2\2\u0a62\u0a63\3\2\2\2\u0a63\u0a65\3\2\2\2\u0a64\u0a66\5\u0202"+
		"\u0102\2\u0a65\u0a64\3\2\2\2\u0a65\u0a66\3\2\2\2\u0a66\u0ba9\3\2\2\2\u0a67"+
		"\u0a69\7\33\2\2\u0a68\u0a6a\5\u00aaV\2\u0a69\u0a68\3\2\2\2\u0a69\u0a6a"+
		"\3\2\2\2\u0a6a\u0a6c\3\2\2\2\u0a6b\u0a6d\5\u0102\u0082\2\u0a6c\u0a6b\3"+
		"\2\2\2\u0a6c\u0a6d\3\2\2\2\u0a6d\u0a6f\3\2\2\2\u0a6e\u0a70\5\u00f8}\2"+
		"\u0a6f\u0a6e\3\2\2\2\u0a6f\u0a70\3\2\2\2\u0a70\u0a72\3\2\2\2\u0a71\u0a73"+
		"\5\u0184\u00c3\2\u0a72\u0a71\3\2\2\2\u0a72\u0a73\3\2\2\2\u0a73\u0ba9\3"+
		"\2\2\2\u0a74\u0a76\7\34\2\2\u0a75\u0a77\5\u00e8u\2\u0a76\u0a75\3\2\2\2"+
		"\u0a76\u0a77\3\2\2\2\u0a77\u0a79\3\2\2\2\u0a78\u0a7a\5X-\2\u0a79\u0a78"+
		"\3\2\2\2\u0a79\u0a7a\3\2\2\2\u0a7a\u0a7c\3\2\2\2\u0a7b\u0a7d\5\u030a\u0186"+
		"\2\u0a7c\u0a7b\3\2\2\2\u0a7c\u0a7d\3\2\2\2\u0a7d\u0a7f\3\2\2\2\u0a7e\u0a80"+
		"\5\u013c\u009f\2\u0a7f\u0a7e\3\2\2\2\u0a7f\u0a80\3\2\2\2\u0a80\u0a82\3"+
		"\2\2\2\u0a81\u0a83\5\u01ee\u00f8\2\u0a82\u0a81\3\2\2\2\u0a82\u0a83\3\2"+
		"\2\2\u0a83\u0a84\3\2\2\2\u0a84\u0ba9\7\u00b5\2\2\u0a85\u0a86\7\35\2\2"+
		"\u0a86\u0ba9\7\u00b5\2\2\u0a87\u0a89\7\36\2\2\u0a88\u0a8a\5\u0120\u0091"+
		"\2\u0a89\u0a88\3\2\2\2\u0a89\u0a8a\3\2\2\2\u0a8a\u0a8c\3\2\2\2\u0a8b\u0a8d"+
		"\5\u0090I\2\u0a8c\u0a8b\3\2\2\2\u0a8c\u0a8d\3\2\2\2\u0a8d\u0a8f\3\2\2"+
		"\2\u0a8e\u0a90\5\u0284\u0143\2\u0a8f\u0a8e\3\2\2\2\u0a8f\u0a90\3\2\2\2"+
		"\u0a90\u0a92\3\2\2\2\u0a91\u0a93\5\f\7\2\u0a92\u0a91\3\2\2\2\u0a92\u0a93"+
		"\3\2\2\2\u0a93\u0a95\3\2\2\2\u0a94\u0a96\5\u02aa\u0156\2\u0a95\u0a94\3"+
		"\2\2\2\u0a95\u0a96\3\2\2\2\u0a96\u0a98\3\2\2\2\u0a97\u0a99\5\u0364\u01b3"+
		"\2\u0a98\u0a97\3\2\2\2\u0a98\u0a99\3\2\2\2\u0a99\u0a9b\3\2\2\2\u0a9a\u0a9c"+
		"\5\u00a6T\2\u0a9b\u0a9a\3\2\2\2\u0a9b\u0a9c\3\2\2\2\u0a9c\u0a9e\3\2\2"+
		"\2\u0a9d\u0a9f\5\u0172\u00ba\2\u0a9e\u0a9d\3\2\2\2\u0a9e\u0a9f\3\2\2\2"+
		"\u0a9f\u0ba9\3\2\2\2\u0aa0\u0aa2\7\37\2\2\u0aa1\u0aa3\5\u01a8\u00d5\2"+
		"\u0aa2\u0aa1\3\2\2\2\u0aa2\u0aa3\3\2\2\2\u0aa3\u0aa5\3\2\2\2\u0aa4\u0aa6"+
		"\5P)\2\u0aa5\u0aa4\3\2\2\2\u0aa5\u0aa6\3\2\2\2\u0aa6\u0aa8\3\2\2\2\u0aa7"+
		"\u0aa9\5\u02e0\u0171\2\u0aa8\u0aa7\3\2\2\2\u0aa8\u0aa9\3\2\2\2\u0aa9\u0aab"+
		"\3\2\2\2\u0aaa\u0aac\5\u0354\u01ab\2\u0aab\u0aaa\3\2\2\2\u0aab\u0aac\3"+
		"\2\2\2\u0aac\u0aae\3\2\2\2\u0aad\u0aaf\5\u0296\u014c\2\u0aae\u0aad\3\2"+
		"\2\2\u0aae\u0aaf\3\2\2\2\u0aaf\u0ab1\3\2\2\2\u0ab0\u0ab2\5\u01ca\u00e6"+
		"\2\u0ab1\u0ab0\3\2\2\2\u0ab1\u0ab2\3\2\2\2\u0ab2\u0ab4\3\2\2\2\u0ab3\u0ab5"+
		"\5\u011c\u008f\2\u0ab4\u0ab3\3\2\2\2\u0ab4\u0ab5\3\2\2\2\u0ab5\u0ab7\3"+
		"\2\2\2\u0ab6\u0ab8\5\u01e0\u00f1\2\u0ab7\u0ab6\3\2\2\2\u0ab7\u0ab8\3\2"+
		"\2\2\u0ab8\u0aba\3\2\2\2\u0ab9\u0abb\5\u02b8\u015d\2\u0aba\u0ab9\3\2\2"+
		"\2\u0aba\u0abb\3\2\2\2\u0abb\u0abd\3\2\2\2\u0abc\u0abe\5\62\32\2\u0abd"+
		"\u0abc\3\2\2\2\u0abd\u0abe\3\2\2\2\u0abe\u0ac0\3\2\2\2\u0abf\u0ac1\5\u024e"+
		"\u0128\2\u0ac0\u0abf\3\2\2\2\u0ac0\u0ac1\3\2\2\2\u0ac1\u0ac3\3\2\2\2\u0ac2"+
		"\u0ac4\5\u0348\u01a5\2\u0ac3\u0ac2\3\2\2\2\u0ac3\u0ac4\3\2\2\2\u0ac4\u0ac6"+
		"\3\2\2\2\u0ac5\u0ac7\5\64\33\2\u0ac6\u0ac5\3\2\2\2\u0ac6\u0ac7\3\2\2\2"+
		"\u0ac7\u0ac9\3\2\2\2\u0ac8\u0aca\5\u0104\u0083\2\u0ac9\u0ac8\3\2\2\2\u0ac9"+
		"\u0aca\3\2\2\2\u0aca\u0acc\3\2\2\2\u0acb\u0acd\5\u02ae\u0158\2\u0acc\u0acb"+
		"\3\2\2\2\u0acc\u0acd\3\2\2\2\u0acd\u0acf\3\2\2\2\u0ace\u0ad0\5\u036a\u01b6"+
		"\2\u0acf\u0ace\3\2\2\2\u0acf\u0ad0\3\2\2\2\u0ad0\u0ad2\3\2\2\2\u0ad1\u0ad3"+
		"\5 \21\2\u0ad2\u0ad1\3\2\2\2\u0ad2\u0ad3\3\2\2\2\u0ad3\u0ad5\3\2\2\2\u0ad4"+
		"\u0ad6\5\u0140\u00a1\2\u0ad5\u0ad4\3\2\2\2\u0ad5\u0ad6\3\2\2\2\u0ad6\u0ad8"+
		"\3\2\2\2\u0ad7\u0ad9\5\u025c\u012f\2\u0ad8\u0ad7\3\2\2\2\u0ad8\u0ad9\3"+
		"\2\2\2\u0ad9\u0adb\3\2\2\2\u0ada\u0adc\5z>\2\u0adb\u0ada\3\2\2\2\u0adb"+
		"\u0adc\3\2\2\2\u0adc\u0ade\3\2\2\2\u0add\u0adf\5\u0366\u01b4\2\u0ade\u0add"+
		"\3\2\2\2\u0ade\u0adf\3\2\2\2\u0adf\u0ae1\3\2\2\2\u0ae0\u0ae2\5\u02b0\u0159"+
		"\2\u0ae1\u0ae0\3\2\2\2\u0ae1\u0ae2\3\2\2\2\u0ae2\u0ae4\3\2\2\2\u0ae3\u0ae5"+
		"\5\u01ba\u00de\2\u0ae4\u0ae3\3\2\2\2\u0ae4\u0ae5\3\2\2\2\u0ae5\u0ae7\3"+
		"\2\2\2\u0ae6\u0ae8\5\u013e\u00a0\2\u0ae7\u0ae6\3\2\2\2\u0ae7\u0ae8\3\2"+
		"\2\2\u0ae8\u0aea\3\2\2\2\u0ae9\u0aeb\5\u0240\u0121\2\u0aea\u0ae9\3\2\2"+
		"\2\u0aea\u0aeb\3\2\2\2\u0aeb\u0aed\3\2\2\2\u0aec\u0aee\5\u02c2\u0162\2"+
		"\u0aed\u0aec\3\2\2\2\u0aed\u0aee\3\2\2\2\u0aee\u0af0\3\2\2\2\u0aef\u0af1"+
		"\5\24\13\2\u0af0\u0aef\3\2\2\2\u0af0\u0af1\3\2\2\2\u0af1\u0af3\3\2\2\2"+
		"\u0af2\u0af4\5\u01b0\u00d9\2\u0af3\u0af2\3\2\2\2\u0af3\u0af4\3\2\2\2\u0af4"+
		"\u0af6\3\2\2\2\u0af5\u0af7\5\u0290\u0149\2\u0af6\u0af5\3\2\2\2\u0af6\u0af7"+
		"\3\2\2\2\u0af7\u0af9\3\2\2\2\u0af8\u0afa\5\u0350\u01a9\2\u0af9\u0af8\3"+
		"\2\2\2\u0af9\u0afa\3\2\2\2\u0afa\u0afc\3\2\2\2\u0afb\u0afd\5\u01f2\u00fa"+
		"\2\u0afc\u0afb\3\2\2\2\u0afc\u0afd\3\2\2\2\u0afd\u0aff\3\2\2\2\u0afe\u0b00"+
		"\5\u019c\u00cf\2\u0aff\u0afe\3\2\2\2\u0aff\u0b00\3\2\2\2\u0b00\u0b02\3"+
		"\2\2\2\u0b01\u0b03\5\u02f2\u017a\2\u0b02\u0b01\3\2\2\2\u0b02\u0b03\3\2"+
		"\2\2\u0b03\u0b05\3\2\2\2\u0b04\u0b06\5\u0088E\2\u0b05\u0b04\3\2\2\2\u0b05"+
		"\u0b06\3\2\2\2\u0b06\u0b08\3\2\2\2\u0b07\u0b09\5\u01d8\u00ed\2\u0b08\u0b07"+
		"\3\2\2\2\u0b08\u0b09\3\2\2\2\u0b09\u0b0b\3\2\2\2\u0b0a\u0b0c\5\u008aF"+
		"\2\u0b0b\u0b0a\3\2\2\2\u0b0b\u0b0c\3\2\2\2\u0b0c\u0b0e\3\2\2\2\u0b0d\u0b0f"+
		"\5\u00a8U\2\u0b0e\u0b0d\3\2\2\2\u0b0e\u0b0f\3\2\2\2\u0b0f\u0b11\3\2\2"+
		"\2\u0b10\u0b12\5Z.\2\u0b11\u0b10\3\2\2\2\u0b11\u0b12\3\2\2\2\u0b12\u0b14"+
		"\3\2\2\2\u0b13\u0b15\5\u030e\u0188\2\u0b14\u0b13\3\2\2\2\u0b14\u0b15\3"+
		"\2\2\2\u0b15\u0b17\3\2\2\2\u0b16\u0b18\5\u02e2\u0172\2\u0b17\u0b16\3\2"+
		"\2\2\u0b17\u0b18\3\2\2\2\u0b18\u0ba9\3\2\2\2\u0b19\u0b1b\7 \2\2\u0b1a"+
		"\u0b1c\5\u033a\u019e\2\u0b1b\u0b1a\3\2\2\2\u0b1b\u0b1c\3\2\2\2\u0b1c\u0b1e"+
		"\3\2\2\2\u0b1d\u0b1f\5\u014e\u00a8\2\u0b1e\u0b1d\3\2\2\2\u0b1e\u0b1f\3"+
		"\2\2\2\u0b1f\u0b21\3\2\2\2\u0b20\u0b22\5\6\4\2\u0b21\u0b20\3\2\2\2\u0b21"+
		"\u0b22\3\2\2\2\u0b22\u0b24\3\2\2\2\u0b23\u0b25\5\u0372\u01ba\2\u0b24\u0b23"+
		"\3\2\2\2\u0b24\u0b25\3\2\2\2\u0b25\u0b27\3\2\2\2\u0b26\u0b28\5\u0136\u009c"+
		"\2\u0b27\u0b26\3\2\2\2\u0b27\u0b28\3\2\2\2\u0b28\u0b2a\3\2\2\2\u0b29\u0b2b"+
		"\5\u013a\u009e\2\u0b2a\u0b29\3\2\2\2\u0b2a\u0b2b\3\2\2\2\u0b2b\u0b2d\3"+
		"\2\2\2\u0b2c\u0b2e\5\u023a\u011e\2\u0b2d\u0b2c\3\2\2\2\u0b2d\u0b2e\3\2"+
		"\2\2\u0b2e\u0b30\3\2\2\2\u0b2f\u0b31\5\u035c\u01af\2\u0b30\u0b2f\3\2\2"+
		"\2\u0b30\u0b31\3\2\2\2\u0b31\u0b33\3\2\2\2\u0b32\u0b34\5\u00d6l\2\u0b33"+
		"\u0b32\3\2\2\2\u0b33\u0b34\3\2\2\2\u0b34\u0b36\3\2\2\2\u0b35\u0b37\5\u0190"+
		"\u00c9\2\u0b36\u0b35\3\2\2\2\u0b36\u0b37\3\2\2\2\u0b37\u0b39\3\2\2\2\u0b38"+
		"\u0b3a\5\u0276\u013c\2\u0b39\u0b38\3\2\2\2\u0b39\u0b3a\3\2\2\2\u0b3a\u0b3c"+
		"\3\2\2\2\u0b3b\u0b3d\5\u01b2\u00da\2\u0b3c\u0b3b\3\2\2\2\u0b3c\u0b3d\3"+
		"\2\2\2\u0b3d\u0b3f\3\2\2\2\u0b3e\u0b40\5\u036c\u01b7\2\u0b3f\u0b3e\3\2"+
		"\2\2\u0b3f\u0b40\3\2\2\2\u0b40\u0b42\3\2\2\2\u0b41\u0b43\5\u00bc_\2\u0b42"+
		"\u0b41\3\2\2\2\u0b42\u0b43\3\2\2\2\u0b43\u0b45\3\2\2\2\u0b44\u0b46\5\u01c2"+
		"\u00e2\2\u0b45\u0b44\3\2\2\2\u0b45\u0b46\3\2\2\2\u0b46\u0b48\3\2\2\2\u0b47"+
		"\u0b49\5\u02a6\u0154\2\u0b48\u0b47\3\2\2\2\u0b48\u0b49\3\2\2\2\u0b49\u0b4b"+
		"\3\2\2\2\u0b4a\u0b4c\5\u0388\u01c5\2\u0b4b\u0b4a\3\2\2\2\u0b4b\u0b4c\3"+
		"\2\2\2\u0b4c\u0b4e\3\2\2\2\u0b4d\u0b4f\5\u01d0\u00e9\2\u0b4e\u0b4d\3\2"+
		"\2\2\u0b4e\u0b4f\3\2\2\2\u0b4f\u0b51\3\2\2\2\u0b50\u0b52\5\20\t\2\u0b51"+
		"\u0b50\3\2\2\2\u0b51\u0b52\3\2\2\2\u0b52\u0b54\3\2\2\2\u0b53\u0b55\5\u0156"+
		"\u00ac\2\u0b54\u0b53\3\2\2\2\u0b54\u0b55\3\2\2\2\u0b55\u0b57\3\2\2\2\u0b56"+
		"\u0b58\5\u0110\u0089\2\u0b57\u0b56\3\2\2\2\u0b57\u0b58\3\2\2\2\u0b58\u0b5a"+
		"\3\2\2\2\u0b59\u0b5b\5\u037e\u01c0\2\u0b5a\u0b59\3\2\2\2\u0b5a\u0b5b\3"+
		"\2\2\2\u0b5b\u0b5d\3\2\2\2\u0b5c\u0b5e\5\u0292\u014a\2\u0b5d\u0b5c\3\2"+
		"\2\2\u0b5d\u0b5e\3\2\2\2\u0b5e\u0b60\3\2\2\2\u0b5f\u0b61\5\u01a0\u00d1"+
		"\2\u0b60\u0b5f\3\2\2\2\u0b60\u0b61\3\2\2\2\u0b61\u0b62\3\2\2\2\u0b62\u0b64"+
		"\7\u00b5\2\2\u0b63\u0b65\5\u02b2\u015a\2\u0b64\u0b63\3\2\2\2\u0b64\u0b65"+
		"\3\2\2\2\u0b65\u0b67\3\2\2\2\u0b66\u0b68\5\u00b4[\2\u0b67\u0b66\3\2\2"+
		"\2\u0b67\u0b68\3\2\2\2\u0b68\u0b6a\3\2\2\2\u0b69\u0b6b\5\u018e\u00c8\2"+
		"\u0b6a\u0b69\3\2\2\2\u0b6a\u0b6b\3\2\2\2\u0b6b\u0ba9\3\2\2\2\u0b6c\u0b6e"+
		"\7!\2\2\u0b6d\u0b6f\5\u038a\u01c6\2\u0b6e\u0b6d\3\2\2\2\u0b6e\u0b6f\3"+
		"\2\2\2\u0b6f\u0b71\3\2\2\2\u0b70\u0b72\5\u024a\u0126\2\u0b71\u0b70\3\2"+
		"\2\2\u0b71\u0b72\3\2\2\2\u0b72\u0b74\3\2\2\2\u0b73\u0b75\5\u00e4s\2\u0b74"+
		"\u0b73\3\2\2\2\u0b74\u0b75\3\2\2\2\u0b75\u0b77\3\2\2\2\u0b76\u0b78\5\u02e4"+
		"\u0173\2\u0b77\u0b76\3\2\2\2\u0b77\u0b78\3\2\2\2\u0b78\u0b7a\3\2\2\2\u0b79"+
		"\u0b7b\5\u00d8m\2\u0b7a\u0b79\3\2\2\2\u0b7a\u0b7b\3\2\2\2\u0b7b\u0b7d"+
		"\3\2\2\2\u0b7c\u0b7e\5\u0146\u00a4\2\u0b7d\u0b7c\3\2\2\2\u0b7d\u0b7e\3"+
		"\2\2\2\u0b7e\u0b80\3\2\2\2\u0b7f\u0b81\5\u02d4\u016b\2\u0b80\u0b7f\3\2"+
		"\2\2\u0b80\u0b81\3\2\2\2\u0b81\u0ba9\3\2\2\2\u0b82\u0b84\7\"\2\2\u0b83"+
		"\u0b85\5> \2\u0b84\u0b83\3\2\2\2\u0b84\u0b85\3\2\2\2\u0b85\u0b87\3\2\2"+
		"\2\u0b86\u0b88\5\u0272\u013a\2\u0b87\u0b86\3\2\2\2\u0b87\u0b88\3\2\2\2"+
		"\u0b88\u0ba9\3\2\2\2\u0b89\u0b8b\7#\2\2\u0b8a\u0b8c\5\u0330\u0199\2\u0b8b"+
		"\u0b8a\3\2\2\2\u0b8b\u0b8c\3\2\2\2\u0b8c\u0b8e\3\2\2\2\u0b8d\u0b8f\7\u00b5"+
		"\2\2\u0b8e\u0b8d\3\2\2\2\u0b8f\u0b90\3\2\2\2\u0b90\u0b8e\3\2\2\2\u0b90"+
		"\u0b91\3\2\2\2\u0b91\u0ba9\3\2\2\2\u0b92\u0b94\7$\2\2\u0b93\u0b95\5\u022c"+
		"\u0117\2\u0b94\u0b93\3\2\2\2\u0b94\u0b95\3\2\2\2\u0b95\u0b97\3\2\2\2\u0b96"+
		"\u0b98\5\u0130\u0099\2\u0b97\u0b96\3\2\2\2\u0b97\u0b98\3\2\2\2\u0b98\u0b9a"+
		"\3\2\2\2\u0b99\u0b9b\5,\27\2\u0b9a\u0b99\3\2\2\2\u0b9a\u0b9b\3\2\2\2\u0b9b"+
		"\u0b9d\3\2\2\2\u0b9c\u0b9e\5\u0144\u00a3\2\u0b9d\u0b9c\3\2\2\2\u0b9d\u0b9e"+
		"\3\2\2\2\u0b9e\u0b9f\3\2\2\2\u0b9f\u0ba0\7\u00b5\2\2\u0ba0\u0ba9\7\u00b5"+
		"\2\2\u0ba1\u0ba3\7%\2\2\u0ba2\u0ba4\5\u0310\u0189\2\u0ba3\u0ba2\3\2\2"+
		"\2\u0ba3\u0ba4\3\2\2\2\u0ba4\u0ba6\3\2\2\2\u0ba5\u0ba7\5\u0092J\2\u0ba6"+
		"\u0ba5\3\2\2\2\u0ba6\u0ba7\3\2\2\2\u0ba7\u0ba9\3\2\2\2\u0ba8\u039a\3\2"+
		"\2\2\u0ba8\u04b1\3\2\2\2\u0ba8\u05c5\3\2\2\2\u0ba8\u05ce\3\2\2\2\u0ba8"+
		"\u05db\3\2\2\2\u0ba8\u0615\3\2\2\2\u0ba8\u0691\3\2\2\2\u0ba8\u070d\3\2"+
		"\2\2\u0ba8\u0722\3\2\2\2\u0ba8\u073b\3\2\2\2\u0ba8\u07b1\3\2\2\2\u0ba8"+
		"\u0819\3\2\2\2\u0ba8\u0877\3\2\2\2\u0ba8\u08c6\3\2\2\2\u0ba8\u0901\3\2"+
		"\2\2\u0ba8\u095a\3\2\2\2\u0ba8\u097f\3\2\2\2\u0ba8\u0990\3\2\2\2\u0ba8"+
		"\u09a9\3\2\2\2\u0ba8\u09b6\3\2\2\2\u0ba8\u09d4\3\2\2\2\u0ba8\u09db\3\2"+
		"\2\2\u0ba8\u09eb\3\2\2\2\u0ba8\u09fb\3\2\2\2\u0ba8\u0a0e\3\2\2\2\u0ba8"+
		"\u0a23\3\2\2\2\u0ba8\u0a38\3\2\2\2\u0ba8\u0a4d\3\2\2\2\u0ba8\u0a60\3\2"+
		"\2\2\u0ba8\u0a67\3\2\2\2\u0ba8\u0a74\3\2\2\2\u0ba8\u0a85\3\2\2\2\u0ba8"+
		"\u0a87\3\2\2\2\u0ba8\u0aa0\3\2\2\2\u0ba8\u0b19\3\2\2\2\u0ba8\u0b6c\3\2"+
		"\2\2\u0ba8\u0b82\3\2\2\2\u0ba8\u0b89\3\2\2\2\u0ba8\u0b92\3\2\2\2\u0ba8"+
		"\u0ba1\3\2\2\2\u0ba9\3\3\2\2\2\u0baa\u0bab\7&\2\2\u0bab\u0bac\7\u00b5"+
		"\2\2\u0bac\5\3\2\2\2\u0bad\u0bae\7\4\2\2\u0bae\7\3\2\2\2\u0baf\u0bb0\7"+
		"\'\2\2\u0bb0\t\3\2\2\2\u0bb1\u0bb2\7(\2\2\u0bb2\13\3\2\2\2\u0bb3\u0bb4"+
		"\7)\2\2\u0bb4\r\3\2\2\2\u0bb5\u0bb6\7\4\2\2\u0bb6\17\3\2\2\2\u0bb7\u0bb8"+
		"\7*\2\2\u0bb8\21\3\2\2\2\u0bb9\u0bba\7+\2\2\u0bba\23\3\2\2\2\u0bbb\u0bbc"+
		"\7,\2\2\u0bbc\25\3\2\2\2\u0bbd\u0bbe\7-\2\2\u0bbe\27\3\2\2\2\u0bbf\u0bc0"+
		"\7.\2\2\u0bc0\u0bc1\7\u00b5\2\2\u0bc1\31\3\2\2\2\u0bc2\u0bc3\7/\2\2\u0bc3"+
		"\u0bc4\7\u00b5\2\2\u0bc4\33\3\2\2\2\u0bc5\u0bc6\7.\2\2\u0bc6\u0bc8\7\u00b5"+
		"\2\2\u0bc7\u0bc9\5\"\22\2\u0bc8\u0bc7\3\2\2\2\u0bc8\u0bc9\3\2\2\2\u0bc9"+
		"\35\3\2\2\2\u0bca\u0bcb\7\60\2\2\u0bcb\u0bcc\7\u00b5\2\2\u0bcc\37\3\2"+
		"\2\2\u0bcd\u0bce\7\'\2\2\u0bce!\3\2\2\2\u0bcf\u0bd0\7\20\2\2\u0bd0#\3"+
		"\2\2\2\u0bd1\u0bd2\7\61\2\2\u0bd2\u0bd3\7\u00b5\2\2\u0bd3%\3\2\2\2\u0bd4"+
		"\u0bd5\7\62\2\2\u0bd5\'\3\2\2\2\u0bd6\u0bd7\7\63\2\2\u0bd7)\3\2\2\2\u0bd8"+
		"\u0bd9\7\64\2\2\u0bd9+\3\2\2\2\u0bda\u0bdb\7\65\2\2\u0bdb-\3\2\2\2\u0bdc"+
		"\u0bdd\7\66\2\2\u0bdd/\3\2\2\2\u0bde\u0bdf\7\64\2\2\u0bdf\61\3\2\2\2\u0be0"+
		"\u0be1\7\67\2\2\u0be1\63\3\2\2\2\u0be2\u0be3\78\2\2\u0be3\65\3\2\2\2\u0be4"+
		"\u0be5\79\2\2\u0be5\u0be6\7\u00b5\2\2\u0be6\67\3\2\2\2\u0be7\u0be8\7:"+
		"\2\2\u0be89\3\2\2\2\u0be9\u0bea\7\4\2\2\u0bea\u0beb\7\u00b5\2\2\u0beb"+
		";\3\2\2\2\u0bec\u0bed\7\62\2\2\u0bed\u0bee\7\u00b5\2\2\u0bee=\3\2\2\2"+
		"\u0bef\u0bf0\7.\2\2\u0bf0?\3\2\2\2\u0bf1\u0bf2\7;\2\2\u0bf2A\3\2\2\2\u0bf3"+
		"\u0bf4\7<\2\2\u0bf4\u0bf5\7\u00b5\2\2\u0bf5C\3\2\2\2\u0bf6\u0bf7\7=\2"+
		"\2\u0bf7E\3\2\2\2\u0bf8\u0bf9\7>\2\2\u0bf9\u0bfa\7\u00b5\2\2\u0bfaG\3"+
		"\2\2\2\u0bfb\u0bfc\7<\2\2\u0bfcI\3\2\2\2\u0bfd\u0bfe\7?\2\2\u0bfeK\3\2"+
		"\2\2\u0bff\u0c00\7@\2\2\u0c00M\3\2\2\2\u0c01\u0c02\7A\2\2\u0c02O\3\2\2"+
		"\2\u0c03\u0c04\7B\2\2\u0c04Q\3\2\2\2\u0c05\u0c07\7\u00b5\2\2\u0c06\u0c05"+
		"\3\2\2\2\u0c07\u0c08\3\2\2\2\u0c08\u0c06\3\2\2\2\u0c08\u0c09\3\2\2\2\u0c09"+
		"S\3\2\2\2\u0c0a\u0c0b\7C\2\2\u0c0bU\3\2\2\2\u0c0c\u0c0d\7D\2\2\u0c0d\u0c0e"+
		"\7\u00b5\2\2\u0c0eW\3\2\2\2\u0c0f\u0c10\7\4\2\2\u0c10\u0c11\7\u00b5\2"+
		"\2\u0c11Y\3\2\2\2\u0c12\u0c13\7\17\2\2\u0c13\u0c14\7\17\2\2\u0c14\u0c15"+
		"\7\u00b5\2\2\u0c15[\3\2\2\2\u0c16\u0c17\7E\2\2\u0c17]\3\2\2\2\u0c18\u0c19"+
		"\7F\2\2\u0c19_\3\2\2\2\u0c1a\u0c1b\7G\2\2\u0c1b\u0c1c\7\u00b5\2\2\u0c1c"+
		"a\3\2\2\2\u0c1d\u0c1e\7H\2\2\u0c1ec\3\2\2\2\u0c1f\u0c20\7;\2\2\u0c20\u0c21"+
		"\7\u00b5\2\2\u0c21e\3\2\2\2\u0c22\u0c23\7I\2\2\u0c23g\3\2\2\2\u0c24\u0c25"+
		"\7J\2\2\u0c25i\3\2\2\2\u0c26\u0c27\7,\2\2\u0c27k\3\2\2\2\u0c28\u0c29\7"+
		"K\2\2\u0c29\u0c2b\7\u00b5\2\2\u0c2a\u0c2c\5\u01fa\u00fe\2\u0c2b\u0c2a"+
		"\3\2\2\2\u0c2b\u0c2c\3\2\2\2\u0c2c\u0c2d\3\2\2\2\u0c2d\u0c2e\7L\2\2\u0c2e"+
		"m\3\2\2\2\u0c2f\u0c30\7\67\2\2\u0c30o\3\2\2\2\u0c31\u0c32\7\4\2\2\u0c32"+
		"\u0c33\7\u00b5\2\2\u0c33q\3\2\2\2\u0c34\u0c35\7)\2\2\u0c35\u0c36\7\u00b5"+
		"\2\2\u0c36s\3\2\2\2\u0c37\u0c39\7\u00b5\2\2\u0c38\u0c37\3\2\2\2\u0c39"+
		"\u0c3a\3\2\2\2\u0c3a\u0c38\3\2\2\2\u0c3a\u0c3b\3\2\2\2\u0c3bu\3\2\2\2"+
		"\u0c3c\u0c3d\7M\2\2\u0c3dw\3\2\2\2\u0c3e\u0c3f\7N\2\2\u0c3fy\3\2\2\2\u0c40"+
		"\u0c41\7\r\2\2\u0c41{\3\2\2\2\u0c42\u0c43\7O\2\2\u0c43}\3\2\2\2\u0c44"+
		"\u0c45\7P\2\2\u0c45\u0c46\7\u00b5\2\2\u0c46\177\3\2\2\2\u0c47\u0c48\7"+
		"Q\2\2\u0c48\u0081\3\2\2\2\u0c49\u0c4a\7R\2\2\u0c4a\u0083\3\2\2\2\u0c4b"+
		"\u0c4c\7+\2\2\u0c4c\u0085\3\2\2\2\u0c4d\u0c4e\7S\2\2\u0c4e\u0087\3\2\2"+
		"\2\u0c4f\u0c50\7T\2\2\u0c50\u0089\3\2\2\2\u0c51\u0c52\7.\2\2\u0c52\u0c53"+
		"\7\u00b5\2\2\u0c53\u008b\3\2\2\2\u0c54\u0c55\t\2\2\2\u0c55\u008d\3\2\2"+
		"\2\u0c56\u0c57\7W\2\2\u0c57\u008f\3\2\2\2\u0c58\u0c59\7X\2\2\u0c59\u0091"+
		"\3\2\2\2\u0c5a\u0c5c\7\u00b5\2\2\u0c5b\u0c5a\3\2\2\2\u0c5c\u0c5d\3\2\2"+
		"\2\u0c5d\u0c5b\3\2\2\2\u0c5d\u0c5e\3\2\2\2\u0c5e\u0093\3\2\2\2\u0c5f\u0c60"+
		"\t\2\2\2\u0c60\u0095\3\2\2\2\u0c61\u0c62\7\16\2\2\u0c62\u0097\3\2\2\2"+
		"\u0c63\u0c64\7U\2\2\u0c64\u0099\3\2\2\2\u0c65\u0c66\7Y\2\2\u0c66\u009b"+
		"\3\2\2\2\u0c67\u0c68\7\u00b5\2\2\u0c68\u009d\3\2\2\2\u0c69\u0c6d\7Z\2"+
		"\2\u0c6a\u0c6c\7\u00b5\2\2\u0c6b\u0c6a\3\2\2\2\u0c6c\u0c6f\3\2\2\2\u0c6d"+
		"\u0c6b\3\2\2\2\u0c6d\u0c6e\3\2\2\2\u0c6e\u009f\3\2\2\2\u0c6f\u0c6d\3\2"+
		"\2\2\u0c70\u0c71\7[\2\2\u0c71\u0c73\7\u00b5\2\2\u0c72\u0c74\5\u01fa\u00fe"+
		"\2\u0c73\u0c72\3\2\2\2\u0c73\u0c74\3\2\2\2\u0c74\u00a1\3\2\2\2\u0c75\u0c76"+
		"\7:\2\2\u0c76\u00a3\3\2\2\2\u0c77\u0c79\7\\\2\2\u0c78\u0c7a\5\u008cG\2"+
		"\u0c79\u0c78\3\2\2\2\u0c79\u0c7a\3\2\2\2\u0c7a\u00a5\3\2\2\2\u0c7b\u0c7c"+
		"\7\64\2\2\u0c7c\u00a7\3\2\2\2\u0c7d\u0c7e\7\17\2\2\u0c7e\u0c7f\7\u00b5"+
		"\2\2\u0c7f\u00a9\3\2\2\2\u0c80\u0c81\t\3\2\2\u0c81\u00ab\3\2\2\2\u0c82"+
		"\u0c83\7\4\2\2\u0c83\u0c84\7\u00b5\2\2\u0c84\u00ad\3\2\2\2\u0c85\u0c86"+
		"\7]\2\2\u0c86\u00af\3\2\2\2\u0c87\u0c88\7^\2\2\u0c88\u00b1\3\2\2\2\u0c89"+
		"\u0c8a\7:\2\2\u0c8a\u00b3\3\2\2\2\u0c8b\u0c8d\7\20\2\2\u0c8c\u0c8e\7\u00b5"+
		"\2\2\u0c8d\u0c8c\3\2\2\2\u0c8e\u0c8f\3\2\2\2\u0c8f\u0c8d\3\2\2\2\u0c8f"+
		"\u0c90\3\2\2\2\u0c90\u00b5\3\2\2\2\u0c91\u0c92\7_\2\2\u0c92\u0c93\7`\2"+
		"\2\u0c93\u0c94\7\u00b5\2\2\u0c94\u00b7\3\2\2\2\u0c95\u0c96\7@\2\2\u0c96"+
		"\u00b9\3\2\2\2\u0c97\u0c98\7J\2\2\u0c98\u00bb\3\2\2\2\u0c99\u0c9a\7.\2"+
		"\2\u0c9a\u00bd\3\2\2\2\u0c9b\u0c9c\t\2\2\2\u0c9c\u00bf\3\2\2\2\u0c9d\u0c9e"+
		"\7a\2\2\u0c9e\u00c1\3\2\2\2\u0c9f\u0ca0\7b\2\2\u0ca0\u00c3\3\2\2\2\u0ca1"+
		"\u0ca2\7c\2\2\u0ca2\u0ca3\7\u00b5\2\2\u0ca3\u00c5\3\2\2\2\u0ca4\u0ca5"+
		"\7d\2\2\u0ca5\u00c7\3\2\2\2\u0ca6\u0ca7\7\67\2\2\u0ca7\u0ca8\7\u00b5\2"+
		"\2\u0ca8\u00c9\3\2\2\2\u0ca9\u0caa\7_\2\2\u0caa\u0cab\7\u00b5\2\2\u0cab"+
		"\u00cb\3\2\2\2\u0cac\u0cad\7e\2\2\u0cad\u00cd\3\2\2\2\u0cae\u0caf\7\'"+
		"\2\2\u0caf\u00cf\3\2\2\2\u0cb0\u0cb1\7f\2\2\u0cb1\u0cb2\7\u00b5\2\2\u0cb2"+
		"\u00d1\3\2\2\2\u0cb3\u0cb4\7Q\2\2\u0cb4\u00d3\3\2\2\2\u0cb5\u0cb6\7\f"+
		"\2\2\u0cb6\u00d5\3\2\2\2\u0cb7\u0cb8\7\64\2\2\u0cb8\u00d7\3\2\2\2\u0cb9"+
		"\u0cba\7\20\2\2\u0cba\u00d9\3\2\2\2\u0cbb\u0cbc\7g\2\2\u0cbc\u0cbd\7\u00b5"+
		"\2\2\u0cbd\u00db\3\2\2\2\u0cbe\u0cbf\7\4\2\2\u0cbf\u0cc0\7\u00b5\2\2\u0cc0"+
		"\u00dd\3\2\2\2\u0cc1\u0cc2\7h\2\2\u0cc2\u0cc3\7\u00b5\2\2\u0cc3\u00df"+
		"\3\2\2\2\u0cc4\u0cc6\5\u02d8\u016d\2\u0cc5\u0cc4\3\2\2\2\u0cc5\u0cc6\3"+
		"\2\2\2\u0cc6\u0cc8\3\2\2\2\u0cc7\u0cc9\5\u008eH\2\u0cc8\u0cc7\3\2\2\2"+
		"\u0cc8\u0cc9\3\2\2\2\u0cc9\u0cce\3\2\2\2\u0cca\u0ccc\5\u01fc\u00ff\2\u0ccb"+
		"\u0cca\3\2\2\2\u0ccb\u0ccc\3\2\2\2\u0ccc\u0cce\3\2\2\2\u0ccd\u0cc5\3\2"+
		"\2\2\u0ccd\u0ccb\3\2\2\2\u0cce\u00e1\3\2\2\2\u0ccf\u0cd0\7<\2\2\u0cd0"+
		"\u00e3\3\2\2\2\u0cd1\u0cd2\7\f\2\2\u0cd2\u00e5\3\2\2\2\u0cd3\u0cd4\7Q"+
		"\2\2\u0cd4\u00e7\3\2\2\2\u0cd5\u0cd6\7,\2\2\u0cd6\u00e9\3\2\2\2\u0cd7"+
		"\u0cd8\7i\2\2\u0cd8\u0cd9\7\u00b5\2\2\u0cd9\u00eb\3\2\2\2\u0cda\u0cdb"+
		"\7\4\2\2\u0cdb\u0cdc\7\u00b5\2\2\u0cdc\u00ed\3\2\2\2\u0cdd\u0cde\7j\2"+
		"\2\u0cde\u0ce0\7\u00b5\2\2\u0cdf\u0ce1\5\u01b6\u00dc\2\u0ce0\u0cdf\3\2"+
		"\2\2\u0ce0\u0ce1\3\2\2\2\u0ce1\u00ef\3\2\2\2\u0ce2\u0ce3\7\17\2\2\u0ce3"+
		"\u00f1\3\2\2\2\u0ce4\u0ce5\7\62\2\2\u0ce5\u00f3\3\2\2\2\u0ce6\u0ce7\7"+
		"k\2\2\u0ce7\u0ce8\7\u00b5\2\2\u0ce8\u00f5\3\2\2\2\u0ce9\u0cea\7\20\2\2"+
		"\u0cea\u00f7\3\2\2\2\u0ceb\u0ced\5\u01e8\u00f5\2\u0cec\u0ceb\3\2\2\2\u0cec"+
		"\u0ced\3\2\2\2\u0ced\u0cf5\3\2\2\2\u0cee\u0cf0\5\u020e\u0108\2\u0cef\u0cee"+
		"\3\2\2\2\u0cef\u0cf0\3\2\2\2\u0cf0\u0cf5\3\2\2\2\u0cf1\u0cf3\5\30\r\2"+
		"\u0cf2\u0cf1\3\2\2\2\u0cf2\u0cf3\3\2\2\2\u0cf3\u0cf5\3\2\2\2\u0cf4\u0cec"+
		"\3\2\2\2\u0cf4\u0cef\3\2\2\2\u0cf4\u0cf2\3\2\2\2\u0cf5\u00f9\3\2\2\2\u0cf6"+
		"\u0cf7\7\'\2\2\u0cf7\u00fb\3\2\2\2\u0cf8\u0cf9\7^\2\2\u0cf9\u00fd\3\2"+
		"\2\2\u0cfa\u0cfb\7W\2\2\u0cfb\u00ff\3\2\2\2\u0cfc\u0cfd\7l\2\2\u0cfd\u0101"+
		"\3\2\2\2\u0cfe\u0cff\7A\2\2\u0cff\u0103\3\2\2\2\u0d00\u0d01\7C\2\2\u0d01"+
		"\u0105\3\2\2\2\u0d02\u0d03\7m\2\2\u0d03\u0d04\7\u00b5\2\2\u0d04\u0107"+
		"\3\2\2\2\u0d05\u0d06\7X\2\2\u0d06\u0109\3\2\2\2\u0d07\u0d08\7;\2\2\u0d08"+
		"\u010b\3\2\2\2\u0d09\u0d0a\7n\2\2\u0d0a\u010d\3\2\2\2\u0d0b\u0d0c\7o\2"+
		"\2\u0d0c\u0d0d\7\u00b5\2\2\u0d0d\u010f\3\2\2\2\u0d0e\u0d0f\7-\2\2\u0d0f"+
		"\u0111\3\2\2\2\u0d10\u0d11\7\66\2\2\u0d11\u0113\3\2\2\2\u0d12\u0d13\7"+
		"<\2\2\u0d13\u0115\3\2\2\2\u0d14\u0d15\7p\2\2\u0d15\u0d16\7\u00b5\2\2\u0d16"+
		"\u0117\3\2\2\2\u0d17\u0d18\7q\2\2\u0d18\u0119\3\2\2\2\u0d19\u0d1a\7r\2"+
		"\2\u0d1a\u011b\3\2\2\2\u0d1b\u0d1c\7X\2\2\u0d1c\u011d\3\2\2\2\u0d1d\u0d1e"+
		"\7s\2\2\u0d1e\u011f\3\2\2\2\u0d1f\u0d20\7n\2\2\u0d20\u0121\3\2\2\2\u0d21"+
		"\u0d22\7\64\2\2\u0d22\u0123\3\2\2\2\u0d23\u0d24\7Q\2\2\u0d24\u0125\3\2"+
		"\2\2\u0d25\u0d26\7t\2\2\u0d26\u0127\3\2\2\2\u0d27\u0d28\7b\2\2\u0d28\u0129"+
		"\3\2\2\2\u0d29\u0d2b\7\u00b5\2\2\u0d2a\u0d29\3\2\2\2\u0d2b\u0d2c\3\2\2"+
		"\2\u0d2c\u0d2a\3\2\2\2\u0d2c\u0d2d\3\2\2\2\u0d2d\u012b\3\2\2\2\u0d2e\u0d2f"+
		"\7V\2\2\u0d2f\u012d\3\2\2\2\u0d30\u0d31\7\4\2\2\u0d31\u012f\3\2\2\2\u0d32"+
		"\u0d33\7u\2\2\u0d33\u0131\3\2\2\2\u0d34\u0d35\7?\2\2\u0d35\u0d36\7\u00b5"+
		"\2\2\u0d36\u0133\3\2\2\2\u0d37\u0d38\7v\2\2\u0d38\u0135\3\2\2\2\u0d39"+
		"\u0d3a\7b\2\2\u0d3a\u0137\3\2\2\2\u0d3b\u0d3c\7w\2\2\u0d3c\u0139\3\2\2"+
		"\2\u0d3d\u0d3e\7\17\2\2\u0d3e\u013b\3\2\2\2\u0d3f\u0d40\7\17\2\2\u0d40"+
		"\u0d41\7\u00b5\2\2\u0d41\u013d\3\2\2\2\u0d42\u0d43\7\16\2\2\u0d43\u013f"+
		"\3\2\2\2\u0d44\u0d45\7+\2\2\u0d45\u0141\3\2\2\2\u0d46\u0d47\7x\2\2\u0d47"+
		"\u0d48\7`\2\2\u0d48\u0d49\7\u00b5\2\2\u0d49\u0143\3\2\2\2\u0d4a\u0d4b"+
		"\7W\2\2\u0d4b\u0145\3\2\2\2\u0d4c\u0d4d\7j\2\2\u0d4d\u0d4e\7\u00b5\2\2"+
		"\u0d4e\u0147\3\2\2\2\u0d4f\u0d50\7Q\2\2\u0d50\u0149\3\2\2\2\u0d51\u0d52"+
		"\7\4\2\2\u0d52\u014b\3\2\2\2\u0d53\u0d55\7\u00b5\2\2\u0d54\u0d53\3\2\2"+
		"\2\u0d55\u0d56\3\2\2\2\u0d56\u0d54\3\2\2\2\u0d56\u0d57\3\2\2\2\u0d57\u014d"+
		"\3\2\2\2\u0d58\u0d59\7\f\2\2\u0d59\u014f\3\2\2\2\u0d5a\u0d5b\7y\2\2\u0d5b"+
		"\u0d5c\7\u00b5\2\2\u0d5c\u0151\3\2\2\2\u0d5d\u0d5e\7z\2\2\u0d5e\u0153"+
		"\3\2\2\2\u0d5f\u0d61\5\u028c\u0147\2\u0d60\u0d5f\3\2\2\2\u0d60\u0d61\3"+
		"\2\2\2\u0d61\u0d69\3\2\2\2\u0d62\u0d64\5\66\34\2\u0d63\u0d62\3\2\2\2\u0d63"+
		"\u0d64\3\2\2\2\u0d64\u0d69\3\2\2\2\u0d65\u0d67\5\u01f6\u00fc\2\u0d66\u0d65"+
		"\3\2\2\2\u0d66\u0d67\3\2\2\2\u0d67\u0d69\3\2\2\2\u0d68\u0d60\3\2\2\2\u0d68"+
		"\u0d63\3\2\2\2\u0d68\u0d66\3\2\2\2\u0d69\u0155\3\2\2\2\u0d6a\u0d6b\7V"+
		"\2\2\u0d6b\u0157\3\2\2\2\u0d6c\u0d6d\7;\2\2\u0d6d\u0159\3\2\2\2\u0d6e"+
		"\u0d6f\7{\2\2\u0d6f\u0d70\7\u00b5\2\2\u0d70\u015b\3\2\2\2\u0d71\u0d72"+
		"\7b\2\2\u0d72\u015d\3\2\2\2\u0d73\u0d74\7\63\2\2\u0d74\u015f\3\2\2\2\u0d75"+
		"\u0d77\7\u00b5\2\2\u0d76\u0d75\3\2\2\2\u0d77\u0d78\3\2\2\2\u0d78\u0d76"+
		"\3\2\2\2\u0d78\u0d79\3\2\2\2\u0d79\u0161\3\2\2\2\u0d7a\u0d7b\7\67\2\2"+
		"\u0d7b\u0163\3\2\2\2\u0d7c\u0d7d\7B\2\2\u0d7d\u0d7e\7\u00b5\2\2\u0d7e"+
		"\u0165\3\2\2\2\u0d7f\u0d80\7|\2\2\u0d80\u0167\3\2\2\2\u0d81\u0d82\7n\2"+
		"\2\u0d82\u0169\3\2\2\2\u0d83\u0d84\7\67\2\2\u0d84\u016b\3\2\2\2\u0d85"+
		"\u0d86\7}\2\2\u0d86\u0d87\7\u00b5\2\2\u0d87\u016d\3\2\2\2\u0d88\u0d89"+
		"\7\66\2\2\u0d89\u016f\3\2\2\2\u0d8a\u0d8b\7\64\2\2\u0d8b\u0171\3\2\2\2"+
		"\u0d8c\u0d8e\7\u00b5\2\2\u0d8d\u0d8c\3\2\2\2\u0d8e\u0d8f\3\2\2\2\u0d8f"+
		"\u0d8d\3\2\2\2\u0d8f\u0d90\3\2\2\2\u0d90\u0173\3\2\2\2\u0d91\u0d92\7~"+
		"\2\2\u0d92\u0175\3\2\2\2\u0d93\u0d94\7)\2\2\u0d94\u0177\3\2\2\2\u0d95"+
		"\u0d96\7j\2\2\u0d96\u0179\3\2\2\2\u0d97\u0d99\7\u00b5\2\2\u0d98\u0d97"+
		"\3\2\2\2\u0d99\u0d9a\3\2\2\2\u0d9a\u0d98\3\2\2\2\u0d9a\u0d9b\3\2\2\2\u0d9b"+
		"\u017b\3\2\2\2\u0d9c\u0d9d\7\u00b5\2\2\u0d9d\u017d\3\2\2\2\u0d9e\u0da0"+
		"\7\\\2\2\u0d9f\u0da1\5\u00be`\2\u0da0\u0d9f\3\2\2\2\u0da0\u0da1\3\2\2"+
		"\2\u0da1\u017f\3\2\2\2\u0da2\u0da3\7\66\2\2\u0da3\u0da4\7\17\2\2\u0da4"+
		"\u0da5\7W\2\2\u0da5\u0da6\7\'\2\2\u0da6\u0da7\7X\2\2\u0da7\u0da8\7\u00b5"+
		"\2\2\u0da8\u0181\3\2\2\2\u0da9\u0daa\7C\2\2\u0daa\u0183\3\2\2\2\u0dab"+
		"\u0dad\7\u00b5\2\2\u0dac\u0dab\3\2\2\2\u0dad\u0dae\3\2\2\2\u0dae\u0dac"+
		"\3\2\2\2\u0dae\u0daf\3\2\2\2\u0daf\u0185\3\2\2\2\u0db0\u0db1\7n\2\2\u0db1"+
		"\u0db2\7\u00b5\2\2\u0db2\u0187\3\2\2\2\u0db3\u0db4\7\177\2\2\u0db4\u0db5"+
		"\7\u00b5\2\2\u0db5\u0189\3\2\2\2\u0db6\u0db7\7\u0080\2\2\u0db7\u0db8\7"+
		"\u00b5\2\2\u0db8\u018b\3\2\2\2\u0db9\u0dba\7\u0081\2\2\u0dba\u0dbb\7\u00b5"+
		"\2\2\u0dbb\u018d\3\2\2\2\u0dbc\u0dbd\7<\2\2\u0dbd\u0dbe\7\u00b5\2\2\u0dbe"+
		"\u018f\3\2\2\2\u0dbf\u0dc0\7\u0082\2\2\u0dc0\u0191\3\2\2\2\u0dc1\u0dc2"+
		"\7\u0083\2\2\u0dc2\u0193\3\2\2\2\u0dc3\u0dc5\7\u00b5\2\2\u0dc4\u0dc3\3"+
		"\2\2\2\u0dc5\u0dc6\3\2\2\2\u0dc6\u0dc4\3\2\2\2\u0dc6\u0dc7\3\2\2\2\u0dc7"+
		"\u0195\3\2\2\2\u0dc8\u0dc9\7\u0084\2\2\u0dc9\u0dca\7\u00b5\2\2\u0dca\u0197"+
		"\3\2\2\2\u0dcb\u0dcc\7n\2\2\u0dcc\u0199\3\2\2\2\u0dcd\u0dce\7\u0085\2"+
		"\2\u0dce\u0dcf\7\u00b5\2\2\u0dcf\u019b\3\2\2\2\u0dd0\u0dd1\7\u0086\2\2"+
		"\u0dd1\u019d\3\2\2\2\u0dd2\u0dd3\7\u0087\2\2\u0dd3\u0dd4\7\u00b5\2\2\u0dd4"+
		"\u019f\3\2\2\2\u0dd5\u0dd6\7M\2\2\u0dd6\u01a1\3\2\2\2\u0dd7\u0dd8\7.\2"+
		"\2\u0dd8\u01a3\3\2\2\2\u0dd9\u0dda\7\u0088\2\2\u0dda\u01a5\3\2\2\2\u0ddb"+
		"\u0ddc\7\u0089\2\2\u0ddc\u0ddd\7\u00b5\2\2\u0ddd\u01a7\3\2\2\2\u0dde\u0ddf"+
		"\7\66\2\2\u0ddf\u01a9\3\2\2\2\u0de0\u0de1\7\17\2\2\u0de1\u01ab\3\2\2\2"+
		"\u0de2\u0de3\7\u008a\2\2\u0de3\u01ad\3\2\2\2\u0de4\u0de5\7\'\2\2\u0de5"+
		"\u01af\3\2\2\2\u0de6\u0de7\7M\2\2\u0de7\u01b1\3\2\2\2\u0de8\u0de9\7n\2"+
		"\2\u0de9\u01b3\3\2\2\2\u0dea\u0deb\7\u008b\2\2\u0deb\u0dec\7\u00b5\2\2"+
		"\u0dec\u01b5\3\2\2\2\u0ded\u0dee\7\\\2\2\u0dee\u0def\7\u00b5\2\2\u0def"+
		"\u01b7\3\2\2\2\u0df0\u0df1\7\\\2\2\u0df1\u01b9\3\2\2\2\u0df2\u0df3\7\62"+
		"\2\2\u0df3\u01bb\3\2\2\2\u0df4\u0df5\7\u008c\2\2\u0df5\u01bd\3\2\2\2\u0df6"+
		"\u0df8\5t;\2\u0df7\u0df6\3\2\2\2\u0df7\u0df8\3\2\2\2\u0df8\u0dfd\3\2\2"+
		"\2\u0df9\u0dfb\5\u0328\u0195\2\u0dfa\u0df9\3\2\2\2\u0dfa\u0dfb\3\2\2\2"+
		"\u0dfb\u0dfd\3\2\2\2\u0dfc\u0df7\3\2\2\2\u0dfc\u0dfa\3\2\2\2\u0dfd\u01bf"+
		"\3\2\2\2\u0dfe\u0dff\7\u008d\2\2\u0dff\u0e00\7\u00b5\2\2\u0e00\u01c1\3"+
		"\2\2\2\u0e01\u0e02\7+\2\2\u0e02\u01c3\3\2\2\2\u0e03\u0e04\7+\2\2\u0e04"+
		"\u01c5\3\2\2\2\u0e05\u0e06\7.\2\2\u0e06\u0e07\7\u00b5\2\2\u0e07\u01c7"+
		"\3\2\2\2\u0e08\u0e09\7\64\2\2\u0e09\u01c9\3\2\2\2\u0e0a\u0e0b\7\u008e"+
		"\2\2\u0e0b\u01cb\3\2\2\2\u0e0c\u0e0d\7b\2\2\u0e0d\u01cd\3\2\2\2\u0e0e"+
		"\u0e0f\7V\2\2\u0e0f\u01cf\3\2\2\2\u0e10\u0e11\7?\2\2\u0e11\u01d1\3\2\2"+
		"\2\u0e12\u0e13\7\u008f\2\2\u0e13\u0e14\7\u00b5\2\2\u0e14\u01d3\3\2\2\2"+
		"\u0e15\u0e16\7\64\2\2\u0e16\u01d5\3\2\2\2\u0e17\u0e18\7\u0090\2\2\u0e18"+
		"\u0e19\7\u00b5\2\2\u0e19\u01d7\3\2\2\2\u0e1a\u0e1b\7n\2\2\u0e1b\u0e1c"+
		"\7\u00b5\2\2\u0e1c\u01d9\3\2\2\2\u0e1d\u0e1e\t\2\2\2\u0e1e\u01db\3\2\2"+
		"\2\u0e1f\u0e20\7\u0091\2\2\u0e20\u0e21\7\u00b5\2\2\u0e21\u01dd\3\2\2\2"+
		"\u0e22\u0e23\7:\2\2\u0e23\u01df\3\2\2\2\u0e24\u0e25\7^\2\2\u0e25\u01e1"+
		"\3\2\2\2\u0e26\u0e27\7\u0092\2\2\u0e27\u01e3\3\2\2\2\u0e28\u0e29\7\'\2"+
		"\2\u0e29\u01e5\3\2\2\2\u0e2a\u0e2b\7\u0093\2\2\u0e2b\u0e2c\7\u00b5\2\2"+
		"\u0e2c\u01e7\3\2\2\2\u0e2d\u0e2e\7n\2\2\u0e2e\u0e2f\7\u00b5\2\2\u0e2f"+
		"\u01e9\3\2\2\2\u0e30\u0e31\7W\2\2\u0e31\u0e32\7\u00b5\2\2\u0e32\u01eb"+
		"\3\2\2\2\u0e33\u0e34\7\u008e\2\2\u0e34\u01ed\3\2\2\2\u0e35\u0e37\7\u00b5"+
		"\2\2\u0e36\u0e38\5\u027c\u013f\2\u0e37\u0e36\3\2\2\2\u0e37\u0e38\3\2\2"+
		"\2\u0e38\u01ef\3\2\2\2\u0e39\u0e3a\7\u0094\2\2\u0e3a\u0e3b\7\u00b5\2\2"+
		"\u0e3b\u01f1\3\2\2\2\u0e3c\u0e3d\7~\2\2\u0e3d\u01f3\3\2\2\2\u0e3e\u0e3f"+
		"\7M\2\2\u0e3f\u0e40\7\u00b5\2\2\u0e40\u01f5\3\2\2\2\u0e41\u0e42\7\u0095"+
		"\2\2\u0e42\u0e43\7\u00b5\2\2\u0e43\u01f7\3\2\2\2\u0e44\u0e45\7^\2\2\u0e45"+
		"\u01f9\3\2\2\2\u0e46\u0e48\7\u00b5\2\2\u0e47\u0e46\3\2\2\2\u0e48\u0e49"+
		"\3\2\2\2\u0e49\u0e47\3\2\2\2\u0e49\u0e4a\3\2\2\2\u0e4a\u01fb\3\2\2\2\u0e4b"+
		"\u0e4c\7.\2\2\u0e4c\u01fd\3\2\2\2\u0e4d\u0e4e\7j\2\2\u0e4e\u01ff\3\2\2"+
		"\2\u0e4f\u0e50\7\u0096\2\2\u0e50\u0e51\7\u00b5\2\2\u0e51\u0201\3\2\2\2"+
		"\u0e52\u0e54\7\u00b5\2\2\u0e53\u0e52\3\2\2\2\u0e54\u0e55\3\2\2\2\u0e55"+
		"\u0e53\3\2\2\2\u0e55\u0e56\3\2\2\2\u0e56\u0203\3\2\2\2\u0e57\u0e58\7\u0097"+
		"\2\2\u0e58\u0205\3\2\2\2\u0e59\u0e5a\7\64\2\2\u0e5a\u0e5b\7\u00b5\2\2"+
		"\u0e5b\u0207\3\2\2\2\u0e5c\u0e5d\7\20\2\2\u0e5d\u0209\3\2\2\2\u0e5e\u0e5f"+
		"\7\u0098\2\2\u0e5f\u0e60\7\u00b5\2\2\u0e60\u020b\3\2\2\2\u0e61\u0e62\7"+
		"A\2\2\u0e62\u020d\3\2\2\2\u0e63\u0e64\7\f\2\2\u0e64\u0e65\7\u00b5\2\2"+
		"\u0e65\u020f\3\2\2\2\u0e66\u0e67\7\u0099\2\2\u0e67\u0211\3\2\2\2\u0e68"+
		"\u0e69\7\u009a\2\2\u0e69\u0213\3\2\2\2\u0e6a\u0e6b\7\u008a\2\2\u0e6b\u0215"+
		"\3\2\2\2\u0e6c\u0e6d\7W\2\2\u0e6d\u0217\3\2\2\2\u0e6e\u0e6f\t\4\2\2\u0e6f"+
		"\u0219\3\2\2\2\u0e70\u0e71\7\4\2\2\u0e71\u0e72\7\u00b5\2\2\u0e72\u021b"+
		"\3\2\2\2\u0e73\u0e74\7\u009b\2\2\u0e74\u021d\3\2\2\2\u0e75\u0e76\7\u0088"+
		"\2\2\u0e76\u021f\3\2\2\2\u0e77\u0e78\7[\2\2\u0e78\u0e7a\7\u00b5\2\2\u0e79"+
		"\u0e7b\5\u01fa\u00fe\2\u0e7a\u0e79\3\2\2\2\u0e7a\u0e7b\3\2\2\2\u0e7b\u0e7c"+
		"\3\2\2\2\u0e7c\u0e7d\7L\2\2\u0e7d\u0221\3\2\2\2\u0e7e\u0e7f\7\u0088\2"+
		"\2\u0e7f\u0223\3\2\2\2\u0e80\u0e81\7\u009c\2\2\u0e81\u0225\3\2\2\2\u0e82"+
		"\u0e83\7\u009d\2\2\u0e83\u0e84\7\u00b5\2\2\u0e84\u0227\3\2\2\2\u0e85\u0e87"+
		"\5\u0382\u01c2\2\u0e86\u0e85\3\2\2\2\u0e86\u0e87\3\2\2\2\u0e87\u0e8c\3"+
		"\2\2\2\u0e88\u0e8a\5\u00dco\2\u0e89\u0e88\3\2\2\2\u0e89\u0e8a\3\2\2\2"+
		"\u0e8a\u0e8c\3\2\2\2\u0e8b\u0e86\3\2\2\2\u0e8b\u0e89\3\2\2\2\u0e8c\u0229"+
		"\3\2\2\2\u0e8d\u0e8e\7Y\2\2\u0e8e\u022b\3\2\2\2\u0e8f\u0e90\7\u009c\2"+
		"\2\u0e90\u022d\3\2\2\2\u0e91\u0e92\7,\2\2\u0e92\u022f\3\2\2\2\u0e93\u0e94"+
		"\7x\2\2\u0e94\u0e95\7\u00b5\2\2\u0e95\u0231\3\2\2\2\u0e96\u0e97\7\u009e"+
		"\2\2\u0e97\u0233\3\2\2\2\u0e98\u0e99\7\63\2\2\u0e99\u0235\3\2\2\2\u0e9a"+
		"\u0e9b\7W\2\2\u0e9b\u0237\3\2\2\2\u0e9c\u0e9d\7\u0082\2\2\u0e9d\u0239"+
		"\3\2\2\2\u0e9e\u0e9f\7\62\2\2\u0e9f\u023b\3\2\2\2\u0ea0\u0ea1\7X\2\2\u0ea1"+
		"\u0ea2\7\u00b5\2\2\u0ea2\u023d\3\2\2\2\u0ea3\u0ea4\7\f\2\2\u0ea4\u023f"+
		"\3\2\2\2\u0ea5\u0ea6\7\64\2\2\u0ea6\u0241\3\2\2\2\u0ea7\u0ea8\7\u00b5"+
		"\2\2\u0ea8\u0243\3\2\2\2\u0ea9\u0eaa\7\\\2\2\u0eaa\u0245\3\2\2\2\u0eab"+
		"\u0eac\7\u009f\2\2\u0eac\u0ead\7\u00b5\2\2\u0ead\u0247\3\2\2\2\u0eae\u0eb0"+
		"\5\u01c6\u00e4\2\u0eaf\u0eae\3\2\2\2\u0eaf\u0eb0\3\2\2\2\u0eb0\u0eb5\3"+
		"\2\2\2\u0eb1\u0eb3\5\u037a\u01be\2\u0eb2\u0eb1\3\2\2\2\u0eb2\u0eb3\3\2"+
		"\2\2\u0eb3\u0eb5\3\2\2\2\u0eb4\u0eaf\3\2\2\2\u0eb4\u0eb2\3\2\2\2\u0eb5"+
		"\u0249\3\2\2\2\u0eb6\u0ebc\7\66\2\2\u0eb7\u0ebc\7)\2\2\u0eb8\u0eba\5B"+
		"\"\2\u0eb9\u0eb8\3\2\2\2\u0eb9\u0eba\3\2\2\2\u0eba\u0ebc\3\2\2\2\u0ebb"+
		"\u0eb6\3\2\2\2\u0ebb\u0eb7\3\2\2\2\u0ebb\u0eb9\3\2\2\2\u0ebc\u024b\3\2"+
		"\2\2\u0ebd\u0ebe\7B\2\2\u0ebe\u024d\3\2\2\2\u0ebf\u0ec0\7(\2\2\u0ec0\u024f"+
		"\3\2\2\2\u0ec1\u0ec2\7\r\2\2\u0ec2\u0251\3\2\2\2\u0ec3\u0ec4\7X\2\2\u0ec4"+
		"\u0ec5\7\u00b5\2\2\u0ec5\u0253\3\2\2\2\u0ec6\u0ec7\7+\2\2\u0ec7\u0255"+
		"\3\2\2\2\u0ec8\u0ec9\7\u00a0\2\2\u0ec9\u0eca\7\u00b5\2\2\u0eca\u0257\3"+
		"\2\2\2\u0ecb\u0ecc\7V\2\2\u0ecc\u0259\3\2\2\2\u0ecd\u0ece\7A\2\2\u0ece"+
		"\u025b\3\2\2\2\u0ecf\u0ed0\7A\2\2\u0ed0\u025d\3\2\2\2\u0ed1\u0ed2\7n\2"+
		"\2\u0ed2\u025f\3\2\2\2\u0ed3\u0ed4\78\2\2\u0ed4\u0261\3\2\2\2\u0ed5\u0ed6"+
		"\7\u00a1\2\2\u0ed6\u0ed7\7\u00b5\2\2\u0ed7\u0263\3\2\2\2\u0ed8\u0ed9\7"+
		"\66\2\2\u0ed9\u0265\3\2\2\2\u0eda\u0edb\7\u00a2\2\2\u0edb\u0edc\7\u00b5"+
		"\2\2\u0edc\u0267\3\2\2\2\u0edd\u0ede\7\u00a3\2\2\u0ede\u0269\3\2\2\2\u0edf"+
		"\u0ee0\7<\2\2\u0ee0\u026b\3\2\2\2\u0ee1\u0ee2\7\66\2\2\u0ee2\u026d\3\2"+
		"\2\2\u0ee3\u0ee4\7\u00a4\2\2\u0ee4\u026f\3\2\2\2\u0ee5\u0ee6\7a\2\2\u0ee6"+
		"\u0271\3\2\2\2\u0ee7\u0ee9\7\u00b5\2\2\u0ee8\u0ee7\3\2\2\2\u0ee9\u0eea"+
		"\3\2\2\2\u0eea\u0ee8\3\2\2\2\u0eea\u0eeb\3\2\2\2\u0eeb\u0273\3\2\2\2\u0eec"+
		"\u0eed\7\u00a0\2\2\u0eed\u0eee\7\u00b5\2\2\u0eee\u0275\3\2\2\2\u0eef\u0ef0"+
		"\7\66\2\2\u0ef0\u0277\3\2\2\2\u0ef1\u0ef2\7?\2\2\u0ef2\u0ef3\7\u00b5\2"+
		"\2\u0ef3\u0279\3\2\2\2\u0ef4\u0ef5\7\17\2\2\u0ef5\u027b\3\2\2\2\u0ef6"+
		"\u0ef7\7\u00b5\2\2\u0ef7\u027d\3\2\2\2\u0ef8\u0ef9\7a\2\2\u0ef9\u027f"+
		"\3\2\2\2\u0efa\u0efb\7_\2\2\u0efb\u0efc\79\2\2\u0efc\u0efd\7\u00b5\2\2"+
		"\u0efd\u0281\3\2\2\2\u0efe\u0eff\7\u0088\2\2\u0eff\u0283\3\2\2\2\u0f00"+
		"\u0f01\7.\2\2\u0f01\u0285\3\2\2\2\u0f02\u0f03\7\u0082\2\2\u0f03\u0287"+
		"\3\2\2\2\u0f04\u0f05\7W\2\2\u0f05\u0289\3\2\2\2\u0f06\u0f07\7\f\2\2\u0f07"+
		"\u028b\3\2\2\2\u0f08\u0f09\7`\2\2\u0f09\u0f0a\7\u00b5\2\2\u0f0a\u028d"+
		"\3\2\2\2\u0f0b\u0f0c\7\63\2\2\u0f0c\u028f\3\2\2\2\u0f0d\u0f0e\7w\2\2\u0f0e"+
		"\u0291\3\2\2\2\u0f0f\u0f10\7r\2\2\u0f10\u0293\3\2\2\2\u0f11\u0f12\7x\2"+
		"\2\u0f12\u0f13\79\2\2\u0f13\u0f14\7\u00b5\2\2\u0f14\u0295\3\2\2\2\u0f15"+
		"\u0f16\7<\2\2\u0f16\u0297\3\2\2\2\u0f17\u0f18\7,\2\2\u0f18\u0299\3\2\2"+
		"\2\u0f19\u0f1a\7+\2\2\u0f1a\u029b\3\2\2\2\u0f1b\u0f1c\7)\2\2\u0f1c\u029d"+
		"\3\2\2\2\u0f1d\u0f1e\7\20\2\2\u0f1e\u0f1f\7\17\2\2\u0f1f\u0f20\7w\2\2"+
		"\u0f20\u0f21\7b\2\2\u0f21\u0f22\7X\2\2\u0f22\u0f23\7\u00b5\2\2\u0f23\u029f"+
		"\3\2\2\2\u0f24\u0f26\7\u00b5\2\2\u0f25\u0f24\3\2\2\2\u0f26\u0f27\3\2\2"+
		"\2\u0f27\u0f25\3\2\2\2\u0f27\u0f28\3\2\2\2\u0f28\u02a1\3\2\2\2\u0f29\u0f2a"+
		"\7^\2\2\u0f2a\u02a3\3\2\2\2\u0f2b\u0f2c\7:\2\2\u0f2c\u02a5\3\2\2\2\u0f2d"+
		"\u0f2e\7A\2\2\u0f2e\u02a7\3\2\2\2\u0f2f\u0f33\7Z\2\2\u0f30\u0f32\7\u00b5"+
		"\2\2\u0f31\u0f30\3\2\2\2\u0f32\u0f35\3\2\2\2\u0f33\u0f31\3\2\2\2\u0f33"+
		"\u0f34\3\2\2\2\u0f34\u02a9\3\2\2\2\u0f35\u0f33\3\2\2\2\u0f36\u0f37\7\17"+
		"\2\2\u0f37\u02ab\3\2\2\2\u0f38\u0f39\7\u00a5\2\2\u0f39\u0f3a\7\u00b5\2"+
		"\2\u0f3a\u02ad\3\2\2\2\u0f3b\u0f3c\7Q\2\2\u0f3c\u02af\3\2\2\2\u0f3d\u0f3e"+
		"\7:\2\2\u0f3e\u02b1\3\2\2\2\u0f3f\u0f41\7\u00b5\2\2\u0f40\u0f3f\3\2\2"+
		"\2\u0f41\u0f42\3\2\2\2\u0f42\u0f40\3\2\2\2\u0f42\u0f43\3\2\2\2\u0f43\u02b3"+
		"\3\2\2\2\u0f44\u0f45\7d\2\2\u0f45\u0f46\7\u00b5\2\2\u0f46\u02b5\3\2\2"+
		"\2\u0f47\u0f48\7\u00a6\2\2\u0f48\u02b7\3\2\2\2\u0f49\u0f4a\7\4\2\2\u0f4a"+
		"\u02b9\3\2\2\2\u0f4b\u0f4c\7\4\2\2\u0f4c\u02bb\3\2\2\2\u0f4d\u0f4e\7+"+
		"\2\2\u0f4e\u02bd\3\2\2\2\u0f4f\u0f50\7A\2\2\u0f50\u02bf\3\2\2\2\u0f51"+
		"\u0f52\7.\2\2\u0f52\u02c1\3\2\2\2\u0f53\u0f54\7v\2\2\u0f54\u02c3\3\2\2"+
		"\2\u0f55\u0f56\7a\2\2\u0f56\u02c5\3\2\2\2\u0f57\u0f58\7\u00a7\2\2\u0f58"+
		"\u02c7\3\2\2\2\u0f59\u0f5a\7J\2\2\u0f5a\u02c9\3\2\2\2\u0f5b\u0f5c\7.\2"+
		"\2\u0f5c\u02cb\3\2\2\2\u0f5d\u0f5e\7\u00a8\2\2\u0f5e\u02cd\3\2\2\2\u0f5f"+
		"\u0f60\7a\2\2\u0f60\u02cf\3\2\2\2\u0f61\u0f62\7\u00a9\2\2\u0f62\u0f63"+
		"\7\u00b5\2\2\u0f63\u02d1\3\2\2\2\u0f64\u0f65\7Y\2\2\u0f65\u02d3\3\2\2"+
		"\2\u0f66\u0f68\7\u00b5\2\2\u0f67\u0f66\3\2\2\2\u0f68\u0f69\3\2\2\2\u0f69"+
		"\u0f67\3\2\2\2\u0f69\u0f6a\3\2\2\2\u0f6a\u02d5\3\2\2\2\u0f6b\u0f6c\7)"+
		"\2\2\u0f6c\u02d7\3\2\2\2\u0f6d\u0f6e\7\4\2\2\u0f6e\u02d9\3\2\2\2\u0f6f"+
		"\u0f70\7)\2\2\u0f70\u02db\3\2\2\2\u0f71\u0f72\7\u00aa\2\2\u0f72\u0f73"+
		"\7\u00b5\2\2\u0f73\u02dd\3\2\2\2\u0f74\u0f75\7.\2\2\u0f75\u02df\3\2\2"+
		"\2\u0f76\u0f77\7{\2\2\u0f77\u02e1\3\2\2\2\u0f78\u0f79\7\u00ab\2\2\u0f79"+
		"\u0f7a\7\u00b5\2\2\u0f7a\u02e3\3\2\2\2\u0f7b\u0f7c\t\5\2\2\u0f7c\u02e5"+
		"\3\2\2\2\u0f7d\u0f7e\7\u00ac\2\2\u0f7e\u02e7\3\2\2\2\u0f7f\u0f80\7b\2"+
		"\2\u0f80\u02e9\3\2\2\2\u0f81\u0f82\7\64\2\2\u0f82\u02eb\3\2\2\2\u0f83"+
		"\u0f84\7.\2\2\u0f84\u02ed\3\2\2\2\u0f85\u0f86\7^\2\2\u0f86\u0f87\7\u00b5"+
		"\2\2\u0f87\u02ef\3\2\2\2\u0f88\u0f89\7@\2\2\u0f89\u0f8a\7\u00b5\2\2\u0f8a"+
		"\u02f1\3\2\2\2\u0f8b\u0f8c\7\u00ad\2\2\u0f8c\u02f3\3\2\2\2\u0f8d\u0f8e"+
		"\7\u00ae\2\2\u0f8e\u0f8f\7\u00b5\2\2\u0f8f\u02f5\3\2\2\2\u0f90\u0f91\7"+
		"j\2\2\u0f91\u02f7\3\2\2\2\u0f92\u0f93\7<\2\2\u0f93\u02f9\3\2\2\2\u0f94"+
		"\u0f95\7,\2\2\u0f95\u02fb\3\2\2\2\u0f96\u0f97\7)\2\2\u0f97\u0f98\7\u00b5"+
		"\2\2\u0f98\u02fd\3\2\2\2\u0f99\u0f9a\7\20\2\2\u0f9a\u02ff\3\2\2\2\u0f9b"+
		"\u0f9c\7)\2\2\u0f9c\u0301\3\2\2\2\u0f9d\u0f9e\7?\2\2\u0f9e\u0f9f\7\u00b5"+
		"\2\2\u0f9f\u0303\3\2\2\2\u0fa0\u0fa2\7\u00b5\2\2\u0fa1\u0fa0\3\2\2\2\u0fa2"+
		"\u0fa3\3\2\2\2\u0fa3\u0fa1\3\2\2\2\u0fa3\u0fa4\3\2\2\2\u0fa4\u0305\3\2"+
		"\2\2\u0fa5\u0fa6\7\16\2\2\u0fa6\u0307\3\2\2\2\u0fa7\u0fa8\7\r\2\2\u0fa8"+
		"\u0309\3\2\2\2\u0fa9\u0faa\7)\2\2\u0faa\u0fab\7\u00b5\2\2\u0fab\u030b"+
		"\3\2\2\2\u0fac\u0fad\7^\2\2\u0fad\u030d\3\2\2\2\u0fae\u0fb0\7\u00b5\2"+
		"\2\u0faf\u0fb1\5\u0194\u00cb\2\u0fb0\u0faf\3\2\2\2\u0fb0\u0fb1\3\2\2\2"+
		"\u0fb1\u030f\3\2\2\2\u0fb2\u0fb4\7\u00b5\2\2\u0fb3\u0fb2\3\2\2\2\u0fb4"+
		"\u0fb5\3\2\2\2\u0fb5\u0fb3\3\2\2\2\u0fb5\u0fb6\3\2\2\2\u0fb6\u0311\3\2"+
		"\2\2\u0fb7\u0fb8\7(\2\2\u0fb8\u0313\3\2\2\2\u0fb9\u0fba\7\\\2\2\u0fba"+
		"\u0315\3\2\2\2\u0fbb\u0fbc\7{\2\2\u0fbc\u0317\3\2\2\2\u0fbd\u0fbe\7\u00af"+
		"\2\2\u0fbe\u0fbf\7\u00b5\2\2\u0fbf\u0319\3\2\2\2\u0fc0\u0fc1\7{\2\2\u0fc1"+
		"\u0fc2\7\u00b5\2\2\u0fc2\u031b\3\2\2\2\u0fc3\u0fc4\7V\2\2\u0fc4\u031d"+
		"\3\2\2\2\u0fc5\u0fc7\7\u00b5\2\2\u0fc6\u0fc5\3\2\2\2\u0fc7\u0fc8\3\2\2"+
		"\2\u0fc8\u0fc6\3\2\2\2\u0fc8\u0fc9\3\2\2\2\u0fc9\u031f\3\2\2\2\u0fca\u0fcb"+
		"\t\6\2\2\u0fcb\u0321\3\2\2\2\u0fcc\u0fcd\7\\\2\2\u0fcd\u0323\3\2\2\2\u0fce"+
		"\u0fcf\7q\2\2\u0fcf\u0325\3\2\2\2\u0fd0\u0fd1\7\u00b0\2\2\u0fd1\u0fd2"+
		"\7\u00b5\2\2\u0fd2\u0327\3\2\2\2\u0fd3\u0fd5\7\u00b5\2\2\u0fd4\u0fd3\3"+
		"\2\2\2\u0fd5\u0fd6\3\2\2\2\u0fd6\u0fd4\3\2\2\2\u0fd6\u0fd7\3\2\2\2\u0fd7"+
		"\u0329\3\2\2\2\u0fd8\u0fd9\7B\2\2\u0fd9\u0fda\7\u00b5\2\2\u0fda\u032b"+
		"\3\2\2\2\u0fdb\u0fdc\7a\2\2\u0fdc\u032d\3\2\2\2\u0fdd\u0fde\7\64\2\2\u0fde"+
		"\u032f\3\2\2\2\u0fdf\u0fe1\7\u00b5\2\2\u0fe0\u0fdf\3\2\2\2\u0fe1\u0fe2"+
		"\3\2\2\2\u0fe2\u0fe0\3\2\2\2\u0fe2\u0fe3\3\2\2\2\u0fe3\u0331\3\2\2\2\u0fe4"+
		"\u0fe5\7V\2\2\u0fe5\u0fe6\7\u00b5\2\2\u0fe6\u0333\3\2\2\2\u0fe7\u0fe8"+
		"\7\f\2\2\u0fe8\u0335\3\2\2\2\u0fe9\u0fea\7U\2\2\u0fea\u0337\3\2\2\2\u0feb"+
		"\u0fec\7r\2\2\u0fec\u0339\3\2\2\2\u0fed\u0fee\7J\2\2\u0fee\u033b\3\2\2"+
		"\2\u0fef\u0ff0\7b\2\2\u0ff0\u033d\3\2\2\2\u0ff1\u0ff2\7\u00b1\2\2\u0ff2"+
		"\u0ff3\7\u00b5\2\2\u0ff3\u033f\3\2\2\2\u0ff4\u0ff5\7\u00b2\2\2\u0ff5\u0ff7"+
		"\7\u00b5\2\2\u0ff6\u0ff8\5\u01fa\u00fe\2\u0ff7\u0ff6\3\2\2\2\u0ff7\u0ff8"+
		"\3\2\2\2\u0ff8\u0ff9\3\2\2\2\u0ff9\u0ffa\7L\2\2\u0ffa\u0341\3\2\2\2\u0ffb"+
		"\u0ffd\7\u00b5\2\2\u0ffc\u0ffb\3\2\2\2\u0ffd\u0ffe\3\2\2\2\u0ffe\u0ffc"+
		"\3\2\2\2\u0ffe\u0fff\3\2\2\2\u0fff\u0343\3\2\2\2\u1000\u1001\7\4\2\2\u1001"+
		"\u0345\3\2\2\2\u1002\u1003\7\66\2\2\u1003\u0347\3\2\2\2\u1004\u1005\7"+
		"a\2\2\u1005\u0349\3\2\2\2\u1006\u1007\7U\2\2\u1007\u034b\3\2\2\2\u1008"+
		"\u1009\7?\2\2\u1009\u034d\3\2\2\2\u100a\u100b\7\20\2\2\u100b\u034f\3\2"+
		"\2\2\u100c\u100d\7\u0082\2\2\u100d\u0351\3\2\2\2\u100e\u100f\7\u008e\2"+
		"\2\u100f\u0353\3\2\2\2\u1010\u1011\7\f\2\2\u1011\u0355\3\2\2\2\u1012\u1013"+
		"\7\f\2\2\u1013\u0357\3\2\2\2\u1014\u1015\7w\2\2\u1015\u0359\3\2\2\2\u1016"+
		"\u1017\7<\2\2\u1017\u035b\3\2\2\2\u1018\u1019\7\16\2\2\u1019\u035d\3\2"+
		"\2\2\u101a\u101b\7U\2\2\u101b\u035f\3\2\2\2\u101c\u101d\7C\2\2\u101d\u0361"+
		"\3\2\2\2\u101e\u101f\7M\2\2\u101f\u0363\3\2\2\2\u1020\u1021\7\16\2\2\u1021"+
		"\u0365\3\2\2\2\u1022\u1023\7\\\2\2\u1023\u0367\3\2\2\2\u1024\u1026\7\u00b5"+
		"\2\2\u1025\u1024\3\2\2\2\u1026\u1027\3\2\2\2\u1027\u1025\3\2\2\2\u1027"+
		"\u1028\3\2\2\2\u1028\u0369\3\2\2\2\u1029\u102a\7V\2\2\u102a\u036b\3\2"+
		"\2\2\u102b\u102c\78\2\2\u102c\u036d\3\2\2\2\u102d\u102e\7\u00b3\2\2\u102e"+
		"\u1030\7\u00b5\2\2\u102f\u1031\5\u01fa\u00fe\2\u1030\u102f\3\2\2\2\u1030"+
		"\u1031\3\2\2\2\u1031\u1033\3\2\2\2\u1032\u1034\7\u00b4\2\2\u1033\u1032"+
		"\3\2\2\2\u1034\u1035\3\2\2\2\u1035\u1033\3\2\2\2\u1035\u1036\3\2\2\2\u1036"+
		"\u036f\3\2\2\2\u1037\u1038\7\'\2\2\u1038\u0371\3\2\2\2\u1039\u103a\7Q"+
		"\2\2\u103a\u0373\3\2\2\2\u103b\u103c\7,\2\2\u103c\u0375\3\2\2\2\u103d"+
		"\u103f\7\\\2\2\u103e\u1040\5\u01da\u00ee\2\u103f\u103e\3\2\2\2\u103f\u1040"+
		"\3\2\2\2\u1040\u0377\3\2\2\2\u1041\u1042\7\17\2\2\u1042\u0379\3\2\2\2"+
		"\u1043\u1044\7\f\2\2\u1044\u1045\7\u00b5\2\2\u1045\u037b\3\2\2\2\u1046"+
		"\u1047\7\r\2\2\u1047\u037d\3\2\2\2\u1048\u1049\7v\2\2\u1049\u037f\3\2"+
		"\2\2\u104a\u104b\7S\2\2\u104b\u104c\7\u00b5\2\2\u104c\u0381\3\2\2\2\u104d"+
		"\u104f\7\u00b5\2\2\u104e\u104d\3\2\2\2\u104f\u1050\3\2\2\2\u1050\u104e"+
		"\3\2\2\2\u1050\u1051\3\2\2\2\u1051\u0383\3\2\2\2\u1052\u1053\7X\2\2\u1053"+
		"\u1054\7\u00b5\2\2\u1054\u0385\3\2\2\2\u1055\u1056\7v\2\2\u1056\u0387"+
		"\3\2\2\2\u1057\u1058\7)\2\2\u1058\u0389\3\2\2\2\u1059\u105a\t\2\2\2\u105a"+
		"\u038b\3\2\2\2\u105b\u105d\7\u00b5\2\2\u105c\u105e\5\u012a\u0096\2\u105d"+
		"\u105c\3\2\2\2\u105d\u105e\3\2\2\2\u105e\u038d\3\2\2\2\u105f\u1060\7\u00b3"+
		"\2\2\u1060\u1062\7\u00b5\2\2\u1061\u1063\5\u01fa\u00fe\2\u1062\u1061\3"+
		"\2\2\2\u1062\u1063\3\2\2\2\u1063\u1064\3\2\2\2\u1064\u1065\7L\2\2\u1065"+
		"\u038f\3\2\2\2\u1066\u1067\7.\2\2\u1067\u0391\3\2\2\2\u1068\u1069\7W\2"+
		"\2\u1069\u0393\3\2\2\2\u106a\u106b\7N\2\2\u106b\u0395\3\2\2\2\u106c\u106d"+
		"\7Q\2\2\u106d\u0397\3\2\2\2\u106e\u106f\7\r\2\2\u106f\u0399\3\2\2\2\u02d6"+
		"\u039c\u039f\u03a2\u03a5\u03a8\u03ab\u03ae\u03b3\u03b6\u03b9\u03bc\u03bf"+
		"\u03c2\u03c5\u03c8\u03cb\u03ce\u03d1\u03d4\u03d7\u03da\u03dd\u03e0\u03e3"+
		"\u03e6\u03e9\u03ec\u03ef\u03f2\u03f5\u03f8\u03fb\u03fe\u0401\u0404\u0407"+
		"\u040a\u040d\u0410\u0413\u0416\u0419\u041c\u041f\u0422\u0425\u0428\u042b"+
		"\u042e\u0431\u0434\u0437\u043a\u043d\u0440\u0443\u0446\u0449\u044c\u044f"+
		"\u0452\u0455\u0458\u045b\u045e\u0461\u0464\u0467\u046a\u046d\u0470\u0473"+
		"\u0476\u0479\u047c\u047f\u0482\u0485\u0488\u048b\u048e\u0491\u0494\u0497"+
		"\u049a\u049d\u04a0\u04a3\u04a6\u04a9\u04ac\u04af\u04b3\u04b6\u04b9\u04bc"+
		"\u04bf\u04c2\u04c7\u04ca\u04cd\u04d0\u04d3\u04d6\u04d9\u04dc\u04df\u04e2"+
		"\u04e5\u04e8\u04eb\u04ee\u04f1\u04f4\u04f7\u04fa\u04fd\u0500\u0503\u0506"+
		"\u0509\u050c\u050f\u0512\u0515\u0518\u051b\u051e\u0521\u0524\u0527\u052a"+
		"\u052d\u0530\u0533\u0536\u0539\u053c\u053f\u0542\u0545\u0548\u054b\u054e"+
		"\u0551\u0554\u0557\u055a\u055d\u0560\u0563\u0566\u0569\u056c\u056f\u0572"+
		"\u0575\u0578\u057b\u057e\u0581\u0584\u0587\u058a\u058d\u0590\u0593\u0596"+
		"\u0599\u059c\u059f\u05a2\u05a5\u05a8\u05ab\u05ae\u05b1\u05b4\u05b7\u05ba"+
		"\u05bd\u05c0\u05c3\u05c7\u05ca\u05d0\u05d3\u05d8\u05dd\u05e0\u05e3\u05e6"+
		"\u05e9\u05ec\u05ef\u05f2\u05f5\u05f8\u05fb\u05fe\u0601\u0604\u0607\u060a"+
		"\u060d\u0610\u0613\u0617\u061a\u061d\u0620\u0623\u0626\u0629\u062c\u062f"+
		"\u0632\u0635\u0638\u063b\u063e\u0641\u0644\u0647\u064a\u064d\u0650\u0653"+
		"\u0656\u0659\u065c\u065f\u0662\u0665\u0668\u066b\u066e\u0671\u0674\u0677"+
		"\u067a\u067d\u0680\u0683\u0686\u0689\u068c\u068f\u0693\u0696\u0699\u069c"+
		"\u069f\u06a2\u06a5\u06a8\u06ab\u06ae\u06b1\u06b4\u06b7\u06ba\u06bd\u06c0"+
		"\u06c3\u06c6\u06c9\u06cc\u06cf\u06d2\u06d5\u06d8\u06db\u06de\u06e1\u06e4"+
		"\u06e7\u06ea\u06ed\u06f0\u06f3\u06f6\u06f9\u06fc\u06ff\u0702\u0705\u0708"+
		"\u070b\u070f\u0712\u0715\u0718\u071b\u071e\u0724\u0727\u072a\u072d\u0730"+
		"\u0733\u0738\u073d\u0740\u0743\u0746\u0749\u074c\u074f\u0752\u0755\u0758"+
		"\u075b\u075e\u0761\u0764\u0767\u076a\u076d\u0770\u0773\u0776\u0779\u077c"+
		"\u077f\u0782\u0785\u0788\u078b\u078e\u0791\u0794\u0797\u079a\u079d\u07a0"+
		"\u07a3\u07a6\u07a9\u07ac\u07af\u07b4\u07b7\u07ba\u07bd\u07c0\u07c3\u07c6"+
		"\u07c9\u07cc\u07cf\u07d2\u07d5\u07d8\u07db\u07de\u07e1\u07e4\u07e7\u07ea"+
		"\u07ed\u07f0\u07f3\u07f6\u07f9\u07fc\u07ff\u0802\u0805\u0808\u080b\u080e"+
		"\u0811\u0814\u0817\u081e\u0821\u0824\u0827\u082a\u082d\u0830\u0833\u0836"+
		"\u0839\u083c\u083f\u0842\u0845\u0848\u084b\u084e\u0851\u0854\u0857\u085a"+
		"\u085d\u0860\u0863\u0866\u0869\u086c\u086f\u0872\u0875\u087c\u087f\u0882"+
		"\u0885\u0888\u088b\u088e\u0891\u0894\u0897\u089a\u089d\u08a0\u08a3\u08a6"+
		"\u08a9\u08ac\u08af\u08b2\u08b5\u08b8\u08bb\u08be\u08c1\u08c4\u08c9\u08cc"+
		"\u08cf\u08d2\u08d5\u08d8\u08db\u08de\u08e1\u08e4\u08e7\u08ea\u08ed\u08f0"+
		"\u08f3\u08f6\u08f9\u08fc\u08ff\u0904\u0907\u090a\u090d\u0910\u0913\u0916"+
		"\u0919\u091c\u091f\u0922\u0925\u0928\u092b\u092e\u0931\u0934\u0937\u093a"+
		"\u093d\u0940\u0943\u0946\u0949\u094c\u094f\u0952\u0955\u0958\u095c\u095f"+
		"\u0962\u0965\u0968\u096b\u096e\u0971\u0974\u0977\u097a\u097d\u0981\u0984"+
		"\u0987\u098a\u098e\u0992\u0995\u0998\u099b\u099e\u09a1\u09a4\u09a7\u09ab"+
		"\u09ae\u09b1\u09b4\u09b8\u09bb\u09be\u09c1\u09c4\u09c7\u09ca\u09cd\u09d2"+
		"\u09d6\u09d9\u09dd\u09e0\u09e3\u09e6\u09e9\u09ed\u09f0\u09f3\u09f9\u09fd"+
		"\u0a00\u0a03\u0a06\u0a0c\u0a10\u0a13\u0a16\u0a19\u0a1c\u0a21\u0a25\u0a28"+
		"\u0a2b\u0a2e\u0a31\u0a36\u0a3a\u0a3d\u0a40\u0a43\u0a46\u0a4b\u0a4f\u0a52"+
		"\u0a55\u0a58\u0a5e\u0a62\u0a65\u0a69\u0a6c\u0a6f\u0a72\u0a76\u0a79\u0a7c"+
		"\u0a7f\u0a82\u0a89\u0a8c\u0a8f\u0a92\u0a95\u0a98\u0a9b\u0a9e\u0aa2\u0aa5"+
		"\u0aa8\u0aab\u0aae\u0ab1\u0ab4\u0ab7\u0aba\u0abd\u0ac0\u0ac3\u0ac6\u0ac9"+
		"\u0acc\u0acf\u0ad2\u0ad5\u0ad8\u0adb\u0ade\u0ae1\u0ae4\u0ae7\u0aea\u0aed"+
		"\u0af0\u0af3\u0af6\u0af9\u0afc\u0aff\u0b02\u0b05\u0b08\u0b0b\u0b0e\u0b11"+
		"\u0b14\u0b17\u0b1b\u0b1e\u0b21\u0b24\u0b27\u0b2a\u0b2d\u0b30\u0b33\u0b36"+
		"\u0b39\u0b3c\u0b3f\u0b42\u0b45\u0b48\u0b4b\u0b4e\u0b51\u0b54\u0b57\u0b5a"+
		"\u0b5d\u0b60\u0b64\u0b67\u0b6a\u0b6e\u0b71\u0b74\u0b77\u0b7a\u0b7d\u0b80"+
		"\u0b84\u0b87\u0b8b\u0b90\u0b94\u0b97\u0b9a\u0b9d\u0ba3\u0ba6\u0ba8\u0bc8"+
		"\u0c08\u0c2b\u0c3a\u0c5d\u0c6d\u0c73\u0c79\u0c8f\u0cc5\u0cc8\u0ccb\u0ccd"+
		"\u0ce0\u0cec\u0cef\u0cf2\u0cf4\u0d2c\u0d56\u0d60\u0d63\u0d66\u0d68\u0d78"+
		"\u0d8f\u0d9a\u0da0\u0dae\u0dc6\u0df7\u0dfa\u0dfc\u0e37\u0e49\u0e55\u0e7a"+
		"\u0e86\u0e89\u0e8b\u0eaf\u0eb2\u0eb4\u0eb9\u0ebb\u0eea\u0f27\u0f33\u0f42"+
		"\u0f69\u0fa3\u0fb0\u0fb5\u0fc8\u0fd6\u0fe2\u0ff7\u0ffe\u1027\u1030\u1035"+
		"\u103f\u1050\u105d\u1062";
	public static final String _serializedATN = Utils.join(
		new String[] {
			_serializedATNSegment0,
			_serializedATNSegment1
		},
		""
	);
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}