// Generated from /Users/clwang/Research/commandline-helper/commandline-helper/parsers/command_parser/src/commands.parser/commands.g4 by ANTLR 4.5.3
package cmd_parser.parser;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link commandsParser}.
 */
public interface commandsListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link commandsParser#command}.
	 * @param ctx the parse tree
	 */
	void enterCommand(commandsParser.CommandContext ctx);
	/**
	 * Exit a parse tree produced by {@link commandsParser#command}.
	 * @param ctx the parse tree
	 */
	void exitCommand(commandsParser.CommandContext ctx);
	/**
	 * Enter a parse tree produced by {@link commandsParser#mv}.
	 * @param ctx the parse tree
	 */
	void enterMv(commandsParser.MvContext ctx);
	/**
	 * Exit a parse tree produced by {@link commandsParser#mv}.
	 * @param ctx the parse tree
	 */
	void exitMv(commandsParser.MvContext ctx);
	/**
	 * Enter a parse tree produced by {@link commandsParser#mv_options}.
	 * @param ctx the parse tree
	 */
	void enterMv_options(commandsParser.Mv_optionsContext ctx);
	/**
	 * Exit a parse tree produced by {@link commandsParser#mv_options}.
	 * @param ctx the parse tree
	 */
	void exitMv_options(commandsParser.Mv_optionsContext ctx);
	/**
	 * Enter a parse tree produced by {@link commandsParser#mv_op1}.
	 * @param ctx the parse tree
	 */
	void enterMv_op1(commandsParser.Mv_op1Context ctx);
	/**
	 * Exit a parse tree produced by {@link commandsParser#mv_op1}.
	 * @param ctx the parse tree
	 */
	void exitMv_op1(commandsParser.Mv_op1Context ctx);
	/**
	 * Enter a parse tree produced by {@link commandsParser#mv_op2}.
	 * @param ctx the parse tree
	 */
	void enterMv_op2(commandsParser.Mv_op2Context ctx);
	/**
	 * Exit a parse tree produced by {@link commandsParser#mv_op2}.
	 * @param ctx the parse tree
	 */
	void exitMv_op2(commandsParser.Mv_op2Context ctx);
	/**
	 * Enter a parse tree produced by {@link commandsParser#path}.
	 * @param ctx the parse tree
	 */
	void enterPath(commandsParser.PathContext ctx);
	/**
	 * Exit a parse tree produced by {@link commandsParser#path}.
	 * @param ctx the parse tree
	 */
	void exitPath(commandsParser.PathContext ctx);
}