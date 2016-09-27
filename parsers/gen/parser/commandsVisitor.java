// Generated from /Users/clwang/Research/commandline-helper/commandline-helper/parsers/command_parser/src/commands.parser/commands.g4 by ANTLR 4.5.3
package cmd_parser.parser;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link commandsParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface commandsVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link commandsParser#command}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCommand(commandsParser.CommandContext ctx);
	/**
	 * Visit a parse tree produced by {@link commandsParser#mv}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMv(commandsParser.MvContext ctx);
	/**
	 * Visit a parse tree produced by {@link commandsParser#mv_options}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMv_options(commandsParser.Mv_optionsContext ctx);
	/**
	 * Visit a parse tree produced by {@link commandsParser#mv_op1}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMv_op1(commandsParser.Mv_op1Context ctx);
	/**
	 * Visit a parse tree produced by {@link commandsParser#mv_op2}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMv_op2(commandsParser.Mv_op2Context ctx);
	/**
	 * Visit a parse tree produced by {@link commandsParser#path}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPath(commandsParser.PathContext ctx);
}