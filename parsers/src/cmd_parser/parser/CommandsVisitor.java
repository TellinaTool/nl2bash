// Generated from Commands.g4 by ANTLR 4.5.3
package cmd_parser.parser;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link CommandsParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface CommandsVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link CommandsParser#command}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCommand(CommandsParser.CommandContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#primitive_command}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrimitive_command(CommandsParser.Primitive_commandContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind1(CommandsParser.Find1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind2(CommandsParser.Find2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#mv1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMv1(CommandsParser.Mv1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#mv2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMv2(CommandsParser.Mv2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#mv3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMv3(CommandsParser.Mv3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort1(CommandsParser.Sort1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep1(CommandsParser.Grep1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep1(CommandsParser.Egrep1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cp1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCp1(CommandsParser.Cp1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cp2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCp2(CommandsParser.Cp2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs1(CommandsParser.Ls1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar1(CommandsParser.Tar1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar2(CommandsParser.Tar2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar3(CommandsParser.Tar3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar4(CommandsParser.Tar4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar5(CommandsParser.Tar5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs1(CommandsParser.Xargs1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs2(CommandsParser.Xargs2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sed1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSed1(CommandsParser.Sed1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sed2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSed2(CommandsParser.Sed2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#awk1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAwk1(CommandsParser.Awk1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#rm1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRm1(CommandsParser.Rm1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cd1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCd1(CommandsParser.Cd1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#wc1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWc1(CommandsParser.Wc1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod1(CommandsParser.Chmod1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod2(CommandsParser.Chmod2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod3(CommandsParser.Chmod3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod4(CommandsParser.Chmod4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod5(CommandsParser.Chmod5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chown1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChown1(CommandsParser.Chown1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chgrp1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChgrp1(CommandsParser.Chgrp1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#head1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHead1(CommandsParser.Head1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tail1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTail1(CommandsParser.Tail1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#seq1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSeq1(CommandsParser.Seq1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unlink1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnlink1(CommandsParser.Unlink1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cat1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCat1(CommandsParser.Cat1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip1(CommandsParser.Zip1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip1(CommandsParser.Unzip1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#du1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDu1(CommandsParser.Du1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#echo1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEcho1(CommandsParser.Echo1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#diff1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDiff1(CommandsParser.Diff1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#comm1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComm1(CommandsParser.Comm1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sh1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSh1(CommandsParser.Sh1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op18}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op18(CommandsParser.Find_primitive_exp_op18Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op19}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op19(CommandsParser.Find_primitive_exp_op19Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op14}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op14(CommandsParser.Find_primitive_exp_op14Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op58}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op58(CommandsParser.Find_primitive_exp_op58Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op15}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op15(CommandsParser.Find_primitive_exp_op15Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op59}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op59(CommandsParser.Find_primitive_exp_op59Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op16}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op16(CommandsParser.Find_primitive_exp_op16Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op17}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op17(CommandsParser.Find_primitive_exp_op17Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op10}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op10(CommandsParser.Find_primitive_exp_op10Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op54}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op54(CommandsParser.Find_primitive_exp_op54Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op11}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op11(CommandsParser.Find_primitive_exp_op11Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op55}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op55(CommandsParser.Find_primitive_exp_op55Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op12}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op12(CommandsParser.Find_primitive_exp_op12Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op56}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op56(CommandsParser.Find_primitive_exp_op56Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op13}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op13(CommandsParser.Find_primitive_exp_op13Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op57}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op57(CommandsParser.Find_primitive_exp_op57Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op61}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op61(CommandsParser.Find_primitive_exp_op61Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op62}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op62(CommandsParser.Find_primitive_exp_op62Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op63}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op63(CommandsParser.Find_primitive_exp_op63Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op20}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op20(CommandsParser.Find_primitive_exp_op20Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op64}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op64(CommandsParser.Find_primitive_exp_op64Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op60}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op60(CommandsParser.Find_primitive_exp_op60Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op9}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op9(CommandsParser.Find_primitive_exp_op9Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp(CommandsParser.Find_primitive_expContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op29}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op29(CommandsParser.Find_primitive_exp_op29Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op2(CommandsParser.Find_primitive_exp_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op25}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op25(CommandsParser.Find_primitive_exp_op25Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op69}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op69(CommandsParser.Find_primitive_exp_op69Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op1(CommandsParser.Find_primitive_exp_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op26}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op26(CommandsParser.Find_primitive_exp_op26Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op4(CommandsParser.Find_primitive_exp_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op27}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op27(CommandsParser.Find_primitive_exp_op27Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op3(CommandsParser.Find_primitive_exp_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op28}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op28(CommandsParser.Find_primitive_exp_op28Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op6(CommandsParser.Find_primitive_exp_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op21}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op21(CommandsParser.Find_primitive_exp_op21Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op65}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op65(CommandsParser.Find_primitive_exp_op65Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op5(CommandsParser.Find_primitive_exp_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op22}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op22(CommandsParser.Find_primitive_exp_op22Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op66}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op66(CommandsParser.Find_primitive_exp_op66Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op8}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op8(CommandsParser.Find_primitive_exp_op8Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op23}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op23(CommandsParser.Find_primitive_exp_op23Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op67}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op67(CommandsParser.Find_primitive_exp_op67Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op7(CommandsParser.Find_primitive_exp_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op24}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op24(CommandsParser.Find_primitive_exp_op24Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op68}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op68(CommandsParser.Find_primitive_exp_op68Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_expression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_expression(CommandsParser.Find_expressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op30}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op30(CommandsParser.Find_primitive_exp_op30Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op31}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op31(CommandsParser.Find_primitive_exp_op31Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op0(CommandsParser.Find_primitive_exp_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op70}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op70(CommandsParser.Find_primitive_exp_op70Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op71}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op71(CommandsParser.Find_primitive_exp_op71Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op36}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op36(CommandsParser.Find_primitive_exp_op36Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op37}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op37(CommandsParser.Find_primitive_exp_op37Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op38}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op38(CommandsParser.Find_primitive_exp_op38Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op39}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op39(CommandsParser.Find_primitive_exp_op39Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op32}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op32(CommandsParser.Find_primitive_exp_op32Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op33}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op33(CommandsParser.Find_primitive_exp_op33Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op34}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op34(CommandsParser.Find_primitive_exp_op34Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op35}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op35(CommandsParser.Find_primitive_exp_op35Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op40}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op40(CommandsParser.Find_primitive_exp_op40Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op41}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op41(CommandsParser.Find_primitive_exp_op41Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op42}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op42(CommandsParser.Find_primitive_exp_op42Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op47}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op47(CommandsParser.Find_primitive_exp_op47Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op48}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op48(CommandsParser.Find_primitive_exp_op48Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op49}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op49(CommandsParser.Find_primitive_exp_op49Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op43}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op43(CommandsParser.Find_primitive_exp_op43Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op44}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op44(CommandsParser.Find_primitive_exp_op44Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op45}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op45(CommandsParser.Find_primitive_exp_op45Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op46}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op46(CommandsParser.Find_primitive_exp_op46Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op50}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op50(CommandsParser.Find_primitive_exp_op50Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op51}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op51(CommandsParser.Find_primitive_exp_op51Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op52}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op52(CommandsParser.Find_primitive_exp_op52Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_primitive_exp_op53}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_primitive_exp_op53(CommandsParser.Find_primitive_exp_op53Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_exp_list}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_exp_list(CommandsParser.Find_exp_listContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#awk_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAwk_op0(CommandsParser.Awk_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#awk_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAwk_op1(CommandsParser.Awk_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#awk_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAwk_op2(CommandsParser.Awk_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#awk_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAwk_op3(CommandsParser.Awk_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#awk_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAwk_op4(CommandsParser.Awk_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#awk_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAwk_op5(CommandsParser.Awk_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cat_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCat_op0(CommandsParser.Cat_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cat_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCat_op1(CommandsParser.Cat_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cat_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCat_op2(CommandsParser.Cat_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cat_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCat_op3(CommandsParser.Cat_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cat_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCat_op4(CommandsParser.Cat_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cat_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCat_op5(CommandsParser.Cat_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cat_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCat_op6(CommandsParser.Cat_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cat_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCat_op7(CommandsParser.Cat_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cd_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCd_op0(CommandsParser.Cd_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cd_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCd_op1(CommandsParser.Cd_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chgrp_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChgrp_op0(CommandsParser.Chgrp_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chgrp_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChgrp_op1(CommandsParser.Chgrp_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chgrp_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChgrp_op2(CommandsParser.Chgrp_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chgrp_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChgrp_op3(CommandsParser.Chgrp_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chgrp_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChgrp_op4(CommandsParser.Chgrp_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op0(CommandsParser.Chmod_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op1(CommandsParser.Chmod_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op10}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op10(CommandsParser.Chmod_op10Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op11}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op11(CommandsParser.Chmod_op11Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op2(CommandsParser.Chmod_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op3(CommandsParser.Chmod_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op4(CommandsParser.Chmod_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op5(CommandsParser.Chmod_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op6(CommandsParser.Chmod_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op7(CommandsParser.Chmod_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op8}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op8(CommandsParser.Chmod_op8Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chmod_op9}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChmod_op9(CommandsParser.Chmod_op9Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chown_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChown_op0(CommandsParser.Chown_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chown_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChown_op1(CommandsParser.Chown_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chown_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChown_op2(CommandsParser.Chown_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chown_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChown_op3(CommandsParser.Chown_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#chown_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitChown_op4(CommandsParser.Chown_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#comm_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComm_op0(CommandsParser.Comm_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#comm_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComm_op1(CommandsParser.Comm_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#comm_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComm_op2(CommandsParser.Comm_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#comm_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComm_op3(CommandsParser.Comm_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cp_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCp_op0(CommandsParser.Cp_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cp_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCp_op1(CommandsParser.Cp_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cp_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCp_op2(CommandsParser.Cp_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cp_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCp_op3(CommandsParser.Cp_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cp_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCp_op4(CommandsParser.Cp_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cp_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCp_op5(CommandsParser.Cp_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#cp_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCp_op6(CommandsParser.Cp_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#diff_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDiff_op0(CommandsParser.Diff_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#du_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDu_op0(CommandsParser.Du_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#du_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDu_op1(CommandsParser.Du_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#du_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDu_op2(CommandsParser.Du_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#du_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDu_op3(CommandsParser.Du_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#du_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDu_op4(CommandsParser.Du_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#du_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDu_op5(CommandsParser.Du_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#du_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDu_op6(CommandsParser.Du_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#du_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDu_op7(CommandsParser.Du_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#echo_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEcho_op0(CommandsParser.Echo_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#echo_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEcho_op1(CommandsParser.Echo_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op0(CommandsParser.Egrep_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op1(CommandsParser.Egrep_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op10}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op10(CommandsParser.Egrep_op10Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op11}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op11(CommandsParser.Egrep_op11Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op12}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op12(CommandsParser.Egrep_op12Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op13}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op13(CommandsParser.Egrep_op13Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op14}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op14(CommandsParser.Egrep_op14Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op15}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op15(CommandsParser.Egrep_op15Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op16}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op16(CommandsParser.Egrep_op16Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op17}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op17(CommandsParser.Egrep_op17Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op18}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op18(CommandsParser.Egrep_op18Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op19}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op19(CommandsParser.Egrep_op19Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op2(CommandsParser.Egrep_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op20}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op20(CommandsParser.Egrep_op20Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op21}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op21(CommandsParser.Egrep_op21Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op22}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op22(CommandsParser.Egrep_op22Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op23}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op23(CommandsParser.Egrep_op23Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op24}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op24(CommandsParser.Egrep_op24Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op25}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op25(CommandsParser.Egrep_op25Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op26}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op26(CommandsParser.Egrep_op26Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op27}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op27(CommandsParser.Egrep_op27Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op28}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op28(CommandsParser.Egrep_op28Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op29}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op29(CommandsParser.Egrep_op29Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op3(CommandsParser.Egrep_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op30}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op30(CommandsParser.Egrep_op30Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op31}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op31(CommandsParser.Egrep_op31Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op32}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op32(CommandsParser.Egrep_op32Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op33}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op33(CommandsParser.Egrep_op33Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op34}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op34(CommandsParser.Egrep_op34Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op35}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op35(CommandsParser.Egrep_op35Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op36}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op36(CommandsParser.Egrep_op36Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op37}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op37(CommandsParser.Egrep_op37Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op38}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op38(CommandsParser.Egrep_op38Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op39}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op39(CommandsParser.Egrep_op39Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op4(CommandsParser.Egrep_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op40}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op40(CommandsParser.Egrep_op40Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op5(CommandsParser.Egrep_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op6(CommandsParser.Egrep_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op7(CommandsParser.Egrep_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op8}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op8(CommandsParser.Egrep_op8Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#egrep_op9}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEgrep_op9(CommandsParser.Egrep_op9Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_op0(CommandsParser.Find_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_op1(CommandsParser.Find_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_op2(CommandsParser.Find_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_op3(CommandsParser.Find_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_op4(CommandsParser.Find_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_op5(CommandsParser.Find_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_op6(CommandsParser.Find_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#find_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFind_op7(CommandsParser.Find_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op0(CommandsParser.Grep_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op1(CommandsParser.Grep_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op10}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op10(CommandsParser.Grep_op10Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op11}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op11(CommandsParser.Grep_op11Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op12}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op12(CommandsParser.Grep_op12Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op13}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op13(CommandsParser.Grep_op13Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op14}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op14(CommandsParser.Grep_op14Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op15}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op15(CommandsParser.Grep_op15Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op16}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op16(CommandsParser.Grep_op16Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op17}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op17(CommandsParser.Grep_op17Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op18}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op18(CommandsParser.Grep_op18Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op19}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op19(CommandsParser.Grep_op19Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op2(CommandsParser.Grep_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op20}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op20(CommandsParser.Grep_op20Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op21}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op21(CommandsParser.Grep_op21Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op22}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op22(CommandsParser.Grep_op22Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op23}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op23(CommandsParser.Grep_op23Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op24}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op24(CommandsParser.Grep_op24Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op25}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op25(CommandsParser.Grep_op25Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op26}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op26(CommandsParser.Grep_op26Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op27}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op27(CommandsParser.Grep_op27Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op28}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op28(CommandsParser.Grep_op28Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op29}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op29(CommandsParser.Grep_op29Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op3(CommandsParser.Grep_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op30}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op30(CommandsParser.Grep_op30Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op31}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op31(CommandsParser.Grep_op31Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op32}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op32(CommandsParser.Grep_op32Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op33}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op33(CommandsParser.Grep_op33Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op34}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op34(CommandsParser.Grep_op34Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op35}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op35(CommandsParser.Grep_op35Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op36}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op36(CommandsParser.Grep_op36Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op37}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op37(CommandsParser.Grep_op37Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op38}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op38(CommandsParser.Grep_op38Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op39}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op39(CommandsParser.Grep_op39Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op4(CommandsParser.Grep_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op40}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op40(CommandsParser.Grep_op40Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op5(CommandsParser.Grep_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op6(CommandsParser.Grep_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op7(CommandsParser.Grep_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op8}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op8(CommandsParser.Grep_op8Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#grep_op9}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGrep_op9(CommandsParser.Grep_op9Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#head_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHead_op0(CommandsParser.Head_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#head_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHead_op1(CommandsParser.Head_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#head_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHead_op2(CommandsParser.Head_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#head_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHead_op3(CommandsParser.Head_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op0(CommandsParser.Ls_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op1(CommandsParser.Ls_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op10}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op10(CommandsParser.Ls_op10Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op11}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op11(CommandsParser.Ls_op11Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op12}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op12(CommandsParser.Ls_op12Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op13}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op13(CommandsParser.Ls_op13Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op14}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op14(CommandsParser.Ls_op14Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op15}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op15(CommandsParser.Ls_op15Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op16}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op16(CommandsParser.Ls_op16Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op17}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op17(CommandsParser.Ls_op17Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op18}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op18(CommandsParser.Ls_op18Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op19}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op19(CommandsParser.Ls_op19Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op2(CommandsParser.Ls_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op20}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op20(CommandsParser.Ls_op20Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op21}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op21(CommandsParser.Ls_op21Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op22}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op22(CommandsParser.Ls_op22Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op23}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op23(CommandsParser.Ls_op23Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op24}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op24(CommandsParser.Ls_op24Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op25}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op25(CommandsParser.Ls_op25Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op26}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op26(CommandsParser.Ls_op26Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op27}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op27(CommandsParser.Ls_op27Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op28}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op28(CommandsParser.Ls_op28Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op29}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op29(CommandsParser.Ls_op29Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op3(CommandsParser.Ls_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op30}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op30(CommandsParser.Ls_op30Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op31}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op31(CommandsParser.Ls_op31Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op32}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op32(CommandsParser.Ls_op32Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op33}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op33(CommandsParser.Ls_op33Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op34}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op34(CommandsParser.Ls_op34Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op35}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op35(CommandsParser.Ls_op35Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op36}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op36(CommandsParser.Ls_op36Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op37}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op37(CommandsParser.Ls_op37Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op38}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op38(CommandsParser.Ls_op38Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op4(CommandsParser.Ls_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op5(CommandsParser.Ls_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op6(CommandsParser.Ls_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op7(CommandsParser.Ls_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op8}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op8(CommandsParser.Ls_op8Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#ls_op9}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLs_op9(CommandsParser.Ls_op9Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#mv_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMv_op0(CommandsParser.Mv_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#mv_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMv_op1(CommandsParser.Mv_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#rm_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRm_op0(CommandsParser.Rm_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#rm_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRm_op1(CommandsParser.Rm_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#rm_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRm_op2(CommandsParser.Rm_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#rm_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRm_op3(CommandsParser.Rm_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#rm_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRm_op4(CommandsParser.Rm_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#rm_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRm_op5(CommandsParser.Rm_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#rm_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRm_op6(CommandsParser.Rm_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#rm_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRm_op7(CommandsParser.Rm_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sed_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSed_op0(CommandsParser.Sed_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sed_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSed_op1(CommandsParser.Sed_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sed_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSed_op2(CommandsParser.Sed_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sed_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSed_op3(CommandsParser.Sed_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sed_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSed_op4(CommandsParser.Sed_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sed_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSed_op5(CommandsParser.Sed_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sed_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSed_op6(CommandsParser.Sed_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sed_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSed_op7(CommandsParser.Sed_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#seq_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSeq_op0(CommandsParser.Seq_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#seq_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSeq_op1(CommandsParser.Seq_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#seq_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSeq_op2(CommandsParser.Seq_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#seq_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSeq_op3(CommandsParser.Seq_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#seq_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSeq_op4(CommandsParser.Seq_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#seq_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSeq_op5(CommandsParser.Seq_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sh_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSh_op0(CommandsParser.Sh_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sh_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSh_op1(CommandsParser.Sh_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op0(CommandsParser.Sort_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op1(CommandsParser.Sort_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op10}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op10(CommandsParser.Sort_op10Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op11}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op11(CommandsParser.Sort_op11Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op12}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op12(CommandsParser.Sort_op12Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op13}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op13(CommandsParser.Sort_op13Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op14}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op14(CommandsParser.Sort_op14Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op15}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op15(CommandsParser.Sort_op15Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op16}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op16(CommandsParser.Sort_op16Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op17}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op17(CommandsParser.Sort_op17Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op18}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op18(CommandsParser.Sort_op18Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op2(CommandsParser.Sort_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op3(CommandsParser.Sort_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op4(CommandsParser.Sort_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op5(CommandsParser.Sort_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op6(CommandsParser.Sort_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op7(CommandsParser.Sort_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op8}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op8(CommandsParser.Sort_op8Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#sort_op9}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSort_op9(CommandsParser.Sort_op9Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tail_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTail_op0(CommandsParser.Tail_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tail_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTail_op1(CommandsParser.Tail_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tail_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTail_op2(CommandsParser.Tail_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tail_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTail_op3(CommandsParser.Tail_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tail_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTail_op4(CommandsParser.Tail_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tail_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTail_op5(CommandsParser.Tail_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tail_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTail_op6(CommandsParser.Tail_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op0(CommandsParser.Tar_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op1(CommandsParser.Tar_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op10}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op10(CommandsParser.Tar_op10Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op11}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op11(CommandsParser.Tar_op11Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op12}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op12(CommandsParser.Tar_op12Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op13}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op13(CommandsParser.Tar_op13Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op14}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op14(CommandsParser.Tar_op14Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op15}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op15(CommandsParser.Tar_op15Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op16}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op16(CommandsParser.Tar_op16Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op17}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op17(CommandsParser.Tar_op17Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op18}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op18(CommandsParser.Tar_op18Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op19}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op19(CommandsParser.Tar_op19Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op2(CommandsParser.Tar_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op20}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op20(CommandsParser.Tar_op20Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op21}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op21(CommandsParser.Tar_op21Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op22}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op22(CommandsParser.Tar_op22Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op23}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op23(CommandsParser.Tar_op23Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op24}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op24(CommandsParser.Tar_op24Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op25}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op25(CommandsParser.Tar_op25Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op26}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op26(CommandsParser.Tar_op26Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op27}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op27(CommandsParser.Tar_op27Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op28}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op28(CommandsParser.Tar_op28Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op29}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op29(CommandsParser.Tar_op29Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op3(CommandsParser.Tar_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op30}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op30(CommandsParser.Tar_op30Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op31}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op31(CommandsParser.Tar_op31Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op32}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op32(CommandsParser.Tar_op32Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op33}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op33(CommandsParser.Tar_op33Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op34}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op34(CommandsParser.Tar_op34Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op35}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op35(CommandsParser.Tar_op35Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op36}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op36(CommandsParser.Tar_op36Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op37}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op37(CommandsParser.Tar_op37Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op38}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op38(CommandsParser.Tar_op38Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op39}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op39(CommandsParser.Tar_op39Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op4(CommandsParser.Tar_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op40}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op40(CommandsParser.Tar_op40Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op41}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op41(CommandsParser.Tar_op41Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op42}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op42(CommandsParser.Tar_op42Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op43}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op43(CommandsParser.Tar_op43Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op44}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op44(CommandsParser.Tar_op44Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op45}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op45(CommandsParser.Tar_op45Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op46}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op46(CommandsParser.Tar_op46Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op47}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op47(CommandsParser.Tar_op47Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op48}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op48(CommandsParser.Tar_op48Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op5(CommandsParser.Tar_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op6(CommandsParser.Tar_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op7(CommandsParser.Tar_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op8}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op8(CommandsParser.Tar_op8Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#tar_op9}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTar_op9(CommandsParser.Tar_op9Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op0(CommandsParser.Unzip_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op1(CommandsParser.Unzip_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op10}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op10(CommandsParser.Unzip_op10Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op11}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op11(CommandsParser.Unzip_op11Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op12}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op12(CommandsParser.Unzip_op12Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op13}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op13(CommandsParser.Unzip_op13Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op14}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op14(CommandsParser.Unzip_op14Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op15}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op15(CommandsParser.Unzip_op15Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op16}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op16(CommandsParser.Unzip_op16Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op17}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op17(CommandsParser.Unzip_op17Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op18}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op18(CommandsParser.Unzip_op18Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op19}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op19(CommandsParser.Unzip_op19Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op2(CommandsParser.Unzip_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op20}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op20(CommandsParser.Unzip_op20Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op21}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op21(CommandsParser.Unzip_op21Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op22}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op22(CommandsParser.Unzip_op22Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op23}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op23(CommandsParser.Unzip_op23Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op24}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op24(CommandsParser.Unzip_op24Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op25}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op25(CommandsParser.Unzip_op25Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op26}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op26(CommandsParser.Unzip_op26Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op3(CommandsParser.Unzip_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op4(CommandsParser.Unzip_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op5(CommandsParser.Unzip_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op6(CommandsParser.Unzip_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op7(CommandsParser.Unzip_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op8}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op8(CommandsParser.Unzip_op8Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#unzip_op9}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnzip_op9(CommandsParser.Unzip_op9Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#wc_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWc_op0(CommandsParser.Wc_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#wc_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWc_op1(CommandsParser.Wc_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#wc_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWc_op2(CommandsParser.Wc_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#wc_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWc_op3(CommandsParser.Wc_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#wc_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitWc_op4(CommandsParser.Wc_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op0(CommandsParser.Xargs_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op1(CommandsParser.Xargs_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op10}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op10(CommandsParser.Xargs_op10Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op11}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op11(CommandsParser.Xargs_op11Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op12}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op12(CommandsParser.Xargs_op12Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op13}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op13(CommandsParser.Xargs_op13Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op14}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op14(CommandsParser.Xargs_op14Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op15}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op15(CommandsParser.Xargs_op15Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op16}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op16(CommandsParser.Xargs_op16Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op17}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op17(CommandsParser.Xargs_op17Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op18}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op18(CommandsParser.Xargs_op18Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op19}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op19(CommandsParser.Xargs_op19Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op2(CommandsParser.Xargs_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op20}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op20(CommandsParser.Xargs_op20Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op21}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op21(CommandsParser.Xargs_op21Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op22}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op22(CommandsParser.Xargs_op22Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op23}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op23(CommandsParser.Xargs_op23Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op24}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op24(CommandsParser.Xargs_op24Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op25}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op25(CommandsParser.Xargs_op25Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op26}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op26(CommandsParser.Xargs_op26Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op27}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op27(CommandsParser.Xargs_op27Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op28}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op28(CommandsParser.Xargs_op28Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op29}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op29(CommandsParser.Xargs_op29Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op3(CommandsParser.Xargs_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op30}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op30(CommandsParser.Xargs_op30Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op31}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op31(CommandsParser.Xargs_op31Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op32}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op32(CommandsParser.Xargs_op32Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op33}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op33(CommandsParser.Xargs_op33Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op34}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op34(CommandsParser.Xargs_op34Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op35}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op35(CommandsParser.Xargs_op35Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op36}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op36(CommandsParser.Xargs_op36Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op37}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op37(CommandsParser.Xargs_op37Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op38}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op38(CommandsParser.Xargs_op38Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op39}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op39(CommandsParser.Xargs_op39Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op4(CommandsParser.Xargs_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op40}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op40(CommandsParser.Xargs_op40Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op41}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op41(CommandsParser.Xargs_op41Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op42}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op42(CommandsParser.Xargs_op42Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op5(CommandsParser.Xargs_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op6(CommandsParser.Xargs_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op7(CommandsParser.Xargs_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op8}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op8(CommandsParser.Xargs_op8Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#xargs_op9}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitXargs_op9(CommandsParser.Xargs_op9Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op0}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op0(CommandsParser.Zip_op0Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op1(CommandsParser.Zip_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op10}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op10(CommandsParser.Zip_op10Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op11}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op11(CommandsParser.Zip_op11Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op12}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op12(CommandsParser.Zip_op12Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op13}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op13(CommandsParser.Zip_op13Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op14}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op14(CommandsParser.Zip_op14Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op15}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op15(CommandsParser.Zip_op15Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op16}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op16(CommandsParser.Zip_op16Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op17}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op17(CommandsParser.Zip_op17Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op18}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op18(CommandsParser.Zip_op18Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op19}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op19(CommandsParser.Zip_op19Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op2(CommandsParser.Zip_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op20}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op20(CommandsParser.Zip_op20Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op21}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op21(CommandsParser.Zip_op21Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op22}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op22(CommandsParser.Zip_op22Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op23}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op23(CommandsParser.Zip_op23Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op24}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op24(CommandsParser.Zip_op24Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op25}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op25(CommandsParser.Zip_op25Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op26}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op26(CommandsParser.Zip_op26Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op27}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op27(CommandsParser.Zip_op27Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op28}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op28(CommandsParser.Zip_op28Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op29}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op29(CommandsParser.Zip_op29Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op3}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op3(CommandsParser.Zip_op3Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op30}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op30(CommandsParser.Zip_op30Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op31}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op31(CommandsParser.Zip_op31Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op32}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op32(CommandsParser.Zip_op32Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op33}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op33(CommandsParser.Zip_op33Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op34}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op34(CommandsParser.Zip_op34Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op35}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op35(CommandsParser.Zip_op35Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op36}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op36(CommandsParser.Zip_op36Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op37}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op37(CommandsParser.Zip_op37Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op38}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op38(CommandsParser.Zip_op38Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op39}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op39(CommandsParser.Zip_op39Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op4}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op4(CommandsParser.Zip_op4Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op40}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op40(CommandsParser.Zip_op40Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op5}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op5(CommandsParser.Zip_op5Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op6}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op6(CommandsParser.Zip_op6Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op7}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op7(CommandsParser.Zip_op7Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op8}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op8(CommandsParser.Zip_op8Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#zip_op9}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZip_op9(CommandsParser.Zip_op9Context ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg_Date}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg_Date(CommandsParser.Arg_DateContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg_File}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg_File(CommandsParser.Arg_FileContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg_Unknown}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg_Unknown(CommandsParser.Arg_UnknownContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg_TarFormat}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg_TarFormat(CommandsParser.Arg_TarFormatContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg_Number}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg_Number(CommandsParser.Arg_NumberContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg_Constant}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg_Constant(CommandsParser.Arg_ConstantContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg_Size}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg_Size(CommandsParser.Arg_SizeContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg_Time}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg_Time(CommandsParser.Arg_TimeContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg_Permission}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg_Permission(CommandsParser.Arg_PermissionContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg_String}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg_String(CommandsParser.Arg_StringContext ctx);
	/**
	 * Visit a parse tree produced by {@link CommandsParser#arg}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArg(CommandsParser.ArgContext ctx);
}