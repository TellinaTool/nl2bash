// Generated from /Users/clwang/Research/commandline-helper/commandline-helper/parsers/command_parser/src/commands.parser/commands.g4 by ANTLR 4.5.3
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
public class commandsParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.5.3", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, ID=6, WS=7;
	public static final int
		RULE_command = 0, RULE_mv = 1, RULE_mv_options = 2, RULE_mv_op1 = 3, RULE_mv_op2 = 4, 
		RULE_path = 5;
	public static final String[] ruleNames = {
		"command", "mv", "mv_options", "mv_op1", "mv_op2", "path"
	};

	private static final String[] _LITERAL_NAMES = {
		null, "'mv'", "'-f'", "'-c'", "'-n'", "'-v'"
	};
	private static final String[] _SYMBOLIC_NAMES = {
		null, null, null, null, null, null, "ID", "WS"
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
	public String getGrammarFileName() { return "commands.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public commandsParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}
	public static class CommandContext extends ParserRuleContext {
		public MvContext mv() {
			return getRuleContext(MvContext.class,0);
		}
		public CommandContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_command; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).enterCommand(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).exitCommand(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof commandsVisitor ) return ((commandsVisitor<? extends T>)visitor).visitCommand(this);
			else return visitor.visitChildren(this);
		}
	}

	public final CommandContext command() throws RecognitionException {
		CommandContext _localctx = new CommandContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_command);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(12);
			mv();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class MvContext extends ParserRuleContext {
		public Mv_optionsContext mv_options() {
			return getRuleContext(Mv_optionsContext.class,0);
		}
		public List<PathContext> path() {
			return getRuleContexts(PathContext.class);
		}
		public PathContext path(int i) {
			return getRuleContext(PathContext.class,i);
		}
		public MvContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mv; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).enterMv(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).exitMv(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof commandsVisitor ) return ((commandsVisitor<? extends T>)visitor).visitMv(this);
			else return visitor.visitChildren(this);
		}
	}

	public final MvContext mv() throws RecognitionException {
		MvContext _localctx = new MvContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_mv);
		try {
			int _alt;
			setState(28);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(14);
				match(T__0);
				setState(15);
				mv_options();
				setState(16);
				path();
				setState(17);
				path();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(19);
				match(T__0);
				setState(20);
				mv_options();
				setState(22); 
				_errHandler.sync(this);
				_alt = 1;
				do {
					switch (_alt) {
					case 1:
						{
						{
						setState(21);
						path();
						}
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					setState(24); 
					_errHandler.sync(this);
					_alt = getInterpreter().adaptivePredict(_input,0,_ctx);
				} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
				setState(26);
				path();
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

	public static class Mv_optionsContext extends ParserRuleContext {
		public List<Mv_op1Context> mv_op1() {
			return getRuleContexts(Mv_op1Context.class);
		}
		public Mv_op1Context mv_op1(int i) {
			return getRuleContext(Mv_op1Context.class,i);
		}
		public List<Mv_op2Context> mv_op2() {
			return getRuleContexts(Mv_op2Context.class);
		}
		public Mv_op2Context mv_op2(int i) {
			return getRuleContext(Mv_op2Context.class,i);
		}
		public Mv_optionsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mv_options; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).enterMv_options(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).exitMv_options(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof commandsVisitor ) return ((commandsVisitor<? extends T>)visitor).visitMv_options(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Mv_optionsContext mv_options() throws RecognitionException {
		Mv_optionsContext _localctx = new Mv_optionsContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_mv_options);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(33);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__1) | (1L << T__2) | (1L << T__3))) != 0)) {
				{
				{
				setState(30);
				mv_op1();
				}
				}
				setState(35);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(39);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__4) {
				{
				{
				setState(36);
				mv_op2();
				}
				}
				setState(41);
				_errHandler.sync(this);
				_la = _input.LA(1);
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

	public static class Mv_op1Context extends ParserRuleContext {
		public Mv_op1Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mv_op1; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).enterMv_op1(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).exitMv_op1(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof commandsVisitor ) return ((commandsVisitor<? extends T>)visitor).visitMv_op1(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Mv_op1Context mv_op1() throws RecognitionException {
		Mv_op1Context _localctx = new Mv_op1Context(_ctx, getState());
		enterRule(_localctx, 6, RULE_mv_op1);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(42);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__1) | (1L << T__2) | (1L << T__3))) != 0)) ) {
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

	public static class Mv_op2Context extends ParserRuleContext {
		public Mv_op2Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_mv_op2; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).enterMv_op2(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).exitMv_op2(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof commandsVisitor ) return ((commandsVisitor<? extends T>)visitor).visitMv_op2(this);
			else return visitor.visitChildren(this);
		}
	}

	public final Mv_op2Context mv_op2() throws RecognitionException {
		Mv_op2Context _localctx = new Mv_op2Context(_ctx, getState());
		enterRule(_localctx, 8, RULE_mv_op2);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(44);
			match(T__4);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class PathContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(commandsParser.ID, 0); }
		public PathContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_path; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).enterPath(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof commandsListener ) ((commandsListener)listener).exitPath(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof commandsVisitor ) return ((commandsVisitor<? extends T>)visitor).visitPath(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PathContext path() throws RecognitionException {
		PathContext _localctx = new PathContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_path);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(46);
			match(ID);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\t\63\4\2\t\2\4\3"+
		"\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3"+
		"\3\3\3\6\3\31\n\3\r\3\16\3\32\3\3\3\3\5\3\37\n\3\3\4\7\4\"\n\4\f\4\16"+
		"\4%\13\4\3\4\7\4(\n\4\f\4\16\4+\13\4\3\5\3\5\3\6\3\6\3\7\3\7\3\7\2\2\b"+
		"\2\4\6\b\n\f\2\3\3\2\4\6\60\2\16\3\2\2\2\4\36\3\2\2\2\6#\3\2\2\2\b,\3"+
		"\2\2\2\n.\3\2\2\2\f\60\3\2\2\2\16\17\5\4\3\2\17\3\3\2\2\2\20\21\7\3\2"+
		"\2\21\22\5\6\4\2\22\23\5\f\7\2\23\24\5\f\7\2\24\37\3\2\2\2\25\26\7\3\2"+
		"\2\26\30\5\6\4\2\27\31\5\f\7\2\30\27\3\2\2\2\31\32\3\2\2\2\32\30\3\2\2"+
		"\2\32\33\3\2\2\2\33\34\3\2\2\2\34\35\5\f\7\2\35\37\3\2\2\2\36\20\3\2\2"+
		"\2\36\25\3\2\2\2\37\5\3\2\2\2 \"\5\b\5\2! \3\2\2\2\"%\3\2\2\2#!\3\2\2"+
		"\2#$\3\2\2\2$)\3\2\2\2%#\3\2\2\2&(\5\n\6\2\'&\3\2\2\2(+\3\2\2\2)\'\3\2"+
		"\2\2)*\3\2\2\2*\7\3\2\2\2+)\3\2\2\2,-\t\2\2\2-\t\3\2\2\2./\7\7\2\2/\13"+
		"\3\2\2\2\60\61\7\b\2\2\61\r\3\2\2\2\6\32\36#)";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}