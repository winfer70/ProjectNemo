# Graph Report - .  (2026-08-15)

## Corpus Check
- 865 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 26714 nodes · 66374 edges · 580 communities detected
- Extraction: 39% EXTRACTED · 61% INFERRED · 0% AMBIGUOUS · INFERRED: 40173 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `assert()` - 311 edges
2. `push()` - 159 edges
3. `tn` - 124 edges
4. `tn` - 124 edges
5. `StatementParser` - 123 edges
6. `ExpressionParser` - 119 edges
7. `Tokenizer` - 116 edges
8. `add()` - 78 edges
9. `add()` - 78 edges
10. `has()` - 77 edges

## Surprising Connections (you probably didn't know these)
- `SQLAlchemy ORM model definitions — imported by all routers and seed_data.py.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `Tracks active device pauses for feeding mode.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `A recurring aquarium care task shown in the calendar.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `Records that a CalendarTask was completed on a specific date.` --uses--> `Base`  [INFERRED]
  api\models\orm.py → api\database.py
- `InfluxDB v2 client — write sensor data, query history.` --uses--> `SensorHistoryPoint`  [INFERRED]
  api\services\influx_client.py → api\models\schemas.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.0
Nodes (1378): abort(), abortHandshake(), abortHandshake$1(), abortHandshakeOrEmitwsClientError(), addAndConvert(), addCommentBefore(), addEndtoBlockProps(), addEventListener() (+1370 more)

### Community 1 - "Community 1"
Cohesion: 0.0
Nodes (843): addComment(), adjustInnerComments(), Agent, applyImportPhase(), ArrowHeadParsingScope, assert(), assertAccessor(), assertAnyTypeAnnotation() (+835 more)

### Community 2 - "Community 2"
Cohesion: 0.0
Nodes (545): add(), addArgumentToBeDeoptimized(), addChunkDependenciesAndGetExternalSideEffectAtoms(), addChunkNamesToModule(), addChunksToBundle(), addEdit(), addJsExtension(), addJsExtensionIfNecessary() (+537 more)

### Community 3 - "Community 3"
Cohesion: 0.0
Nodes (544): add(), addArgumentToBeDeoptimized(), addChunkDependenciesAndGetExternalSideEffectAtoms(), addChunkNamesToModule(), addChunksToBundle(), addEdit(), addJsExtension(), addJsExtensionIfNecessary() (+536 more)

### Community 4 - "Community 4"
Cohesion: 0.01
Nodes (646): adapt(), addNode(), advancePositionWithClone(), advancePositionWithMutation(), alloc(), allocUnsafe(), analyzeBindingsFromOptions(), analyzeNode() (+638 more)

### Community 5 - "Community 5"
Cohesion: 0.01
Nodes (308): abstract(), addBox(), addIfFound(), addIfString(), addListener(), addPointsBelow(), addTick(), afterDatasetsUpdate() (+300 more)

### Community 6 - "Community 6"
Cohesion: 0.01
Nodes (565): addEventListener(), addNode(), addSub(), apply(), applyOptions(), applyTranslation(), assert(), assertNumber() (+557 more)

### Community 7 - "Community 7"
Cohesion: 0.01
Nodes (561): addEventListener(), addNode(), addSub(), apply(), applyOptions(), applyTranslation(), assert(), assertNumber() (+553 more)

### Community 8 - "Community 8"
Cohesion: 0.01
Nodes (259): a(), aa(), addBox(), addElements(), Ae(), afterDatasetsUpdate(), afterDraw(), afterEvent() (+251 more)

### Community 9 - "Community 9"
Cohesion: 0.01
Nodes (259): a(), aa(), addBox(), addElements(), Ae(), afterDatasetsUpdate(), afterDraw(), afterEvent() (+251 more)

### Community 10 - "Community 10"
Cohesion: 0.01
Nodes (416): addEventListener(), addSub(), apply(), applyOptions(), applyTranslation(), assertNumber(), assertType(), assignSlots() (+408 more)

### Community 11 - "Community 11"
Cohesion: 0.01
Nodes (414): addEventListener(), addSub(), apply(), applyOptions(), applyTranslation(), assertNumber(), assertType(), assignSlots() (+406 more)

### Community 12 - "Community 12"
Cohesion: 0.01
Nodes (412): addEventListener(), addSub(), apply(), applyOptions(), applyTranslation(), assertNumber(), assertType(), assignSlots() (+404 more)

### Community 13 - "Community 13"
Cohesion: 0.01
Nodes (410): addEventListener(), addSub(), apply(), applyOptions(), applyTranslation(), assertNumber(), assertType(), assignSlots() (+402 more)

### Community 14 - "Community 14"
Cohesion: 0.01
Nodes (370): _1(), _a(), aa(), ad(), Ae(), af(), ah(), ai() (+362 more)

### Community 15 - "Community 15"
Cohesion: 0.01
Nodes (305): abort(), addEventListener(), analyzeBindingsFromOptions(), analyzeScriptBindings(), assertValidPattern(), AST, attachNamespace(), balanced() (+297 more)

### Community 16 - "Community 16"
Cohesion: 0.02
Nodes (165): aaInnerLoop(), aaInsertLastNodeInCommonAncestor(), aaObtainFormattingElementEntry(), aaObtainFurthestBlock(), aaRecreateElementFromEntry(), aaReplaceFormattingElement(), addressEndTagInBody(), addressStartTagInBody() (+157 more)

### Community 17 - "Community 17"
Cohesion: 0.01
Nodes (319): addEventListener(), addSub(), apply(), applyOptions(), applySSRDirectives(), assertType(), assignSlots(), autoPrefix() (+311 more)

### Community 18 - "Community 18"
Cohesion: 0.02
Nodes (248): A(), a7(), a9(), aa(), ab(), ac(), aD(), ae() (+240 more)

### Community 19 - "Community 19"
Cohesion: 0.01
Nodes (194): adopt(), fulfilled(), HttpsProxyAgent, isDefaultPort(), isHTTPS(), omit(), rejected(), step() (+186 more)

### Community 20 - "Community 20"
Cohesion: 0.02
Nodes (236): A(), aa(), ab(), aC(), ad(), ae(), af(), ai() (+228 more)

### Community 21 - "Community 21"
Cohesion: 0.01
Nodes (202): Base, BaseModel, BaseSettings, BLEConnectionManager, BLE gateway WebSocket connection manager bridging main.py and ha_client.py.  T, _cmd1(), connect(), _doSetChannels() (+194 more)

### Community 22 - "Community 22"
Cohesion: 0.02
Nodes (195): A(), b(), e_(), e3(), e4(), ea, eb(), ec() (+187 more)

### Community 23 - "Community 23"
Cohesion: 0.02
Nodes (195): A(), b(), e_(), e3(), e4(), ea, eb(), ec() (+187 more)

### Community 24 - "Community 24"
Cohesion: 0.01
Nodes (243): applyOptions(), assertNumber(), assertType(), assignSlots(), baseCreateRenderer(), callHook(), callWithAsyncErrorHandling(), callWithErrorHandling() (+235 more)

### Community 25 - "Community 25"
Cohesion: 0.01
Nodes (242): applyOptions(), assertNumber(), assertType(), assignSlots(), baseCreateRenderer(), callHook(), callWithAsyncErrorHandling(), callWithErrorHandling() (+234 more)

### Community 26 - "Community 26"
Cohesion: 0.02
Nodes (175): addNode(), advancePositionWithClone(), advancePositionWithMutation(), assert(), backTrack(), baseCompile(), baseParse(), buildClientSlotFn() (+167 more)

### Community 27 - "Community 27"
Cohesion: 0.02
Nodes (175): addNode(), advancePositionWithClone(), advancePositionWithMutation(), assert(), backTrack(), baseCompile(), baseParse(), buildClientSlotFn() (+167 more)

### Community 28 - "Community 28"
Cohesion: 0.02
Nodes (175): A(), __asyncHydrate(), b(), beforeMount(), beforeUnmount(), beforeUpdate(), C(), created() (+167 more)

### Community 29 - "Community 29"
Cohesion: 0.02
Nodes (173): A(), __asyncHydrate(), b(), beforeMount(), beforeUnmount(), beforeUpdate(), C(), created() (+165 more)

### Community 30 - "Community 30"
Cohesion: 0.01
Nodes (8): NumberLiteral(), numericLiteral(), RegexLiteral(), regExpLiteral(), restElement(), RestProperty(), spreadElement(), SpreadProperty()

### Community 31 - "Community 31"
Cohesion: 0.02
Nodes (169): addNode(), advancePositionWithClone(), advancePositionWithMutation(), assert(), backTrack(), baseCompile(), baseParse(), buildClientSlotFn() (+161 more)

### Community 32 - "Community 32"
Cohesion: 0.02
Nodes (168): addNode(), advancePositionWithClone(), advancePositionWithMutation(), backTrack(), baseCompile(), baseParse(), buildClientSlotFn(), buildDirectiveArgs() (+160 more)

### Community 33 - "Community 33"
Cohesion: 0.02
Nodes (152): addNode(), advancePositionWithClone(), advancePositionWithMutation(), assert(), backTrack(), baseCompile(), baseParse(), buildClientSlotFn() (+144 more)

### Community 34 - "Community 34"
Cohesion: 0.02
Nodes (175): applyOptions(), assignSlots(), baseCreateRenderer(), callHook(), callWithAsyncErrorHandling(), callWithErrorHandling(), cloneIfMounted(), cloneVNode() (+167 more)

### Community 35 - "Community 35"
Cohesion: 0.02
Nodes (147): aggregateErrorMessage(), _arrayLikeToArray(), _arrayWithHoles(), _arrayWithoutHoles(), assertOptions(), _assertThisInitialized(), assertValidHttpProtocolURL(), Axios (+139 more)

### Community 36 - "Community 36"
Cohesion: 0.03
Nodes (159): addTimelineEvent(), adjustI18nResources(), ApiProxy, appendBlockToChain(), appendItemToChain(), appendLocaleToChain(), apply(), baseCompile() (+151 more)

### Community 37 - "Community 37"
Cohesion: 0.03
Nodes (159): addTimelineEvent(), adjustI18nResources(), ApiProxy, appendBlockToChain(), appendItemToChain(), appendLocaleToChain(), apply(), baseCompile() (+151 more)

### Community 38 - "Community 38"
Cohesion: 0.02
Nodes (80): ScriptCompileContext, TypeScope, _arrayLikeToArray(), arrayReduce(), asciiToArray(), asciiWords(), Attribute(), baseSlice() (+72 more)

### Community 39 - "Community 39"
Cohesion: 0.03
Nodes (137): c(), d(), e_(), e2(), e6(), ea(), eb(), ec() (+129 more)

### Community 40 - "Community 40"
Cohesion: 0.02
Nodes (124): _addGrace(), addScopes(), addScopesFromKey(), almostEquals(), _angleBetween(), applyAnimationsDefaults(), applyLayoutsDefaults(), applyScaleDefaults() (+116 more)

### Community 41 - "Community 41"
Cohesion: 0.03
Nodes (125): adjustI18nResources(), appendBlockToChain(), appendItemToChain(), appendLocaleToChain(), apply(), baseCompile(), baseCompile$1(), clearDateTimeFormat() (+117 more)

### Community 42 - "Community 42"
Cohesion: 0.03
Nodes (123): addTimelineEvent(), adjustI18nResources(), ApiProxy, appendBlockToChain(), appendItemToChain(), appendLocaleToChain(), apply(), castToVueI18n() (+115 more)

### Community 43 - "Community 43"
Cohesion: 0.03
Nodes (123): addTimelineEvent(), adjustI18nResources(), ApiProxy, appendBlockToChain(), appendItemToChain(), appendLocaleToChain(), apply(), castToVueI18n() (+115 more)

### Community 44 - "Community 44"
Cohesion: 0.03
Nodes (90): addSub(), apply(), BaseReactiveHandler, batch(), checkIdentityKeys(), cleanupDeps(), cleanupEffect(), computed() (+82 more)

### Community 45 - "Community 45"
Cohesion: 0.03
Nodes (90): addSub(), apply(), BaseReactiveHandler, batch(), checkIdentityKeys(), cleanupDeps(), cleanupEffect(), computed() (+82 more)

### Community 46 - "Community 46"
Cohesion: 0.04
Nodes (108): appendBlockToChain(), appendItemToChain(), appendLocaleToChain(), baseCompile(), baseCompile$1(), checkHtmlMessage(), clearCompileCache(), compile() (+100 more)

### Community 47 - "Community 47"
Cohesion: 0.04
Nodes (107): appendBlockToChain(), appendItemToChain(), appendLocaleToChain(), baseCompile(), baseCompile$1(), checkHtmlMessage(), clearCompileCache(), compile() (+99 more)

### Community 48 - "Community 48"
Cohesion: 0.04
Nodes (96): appendBlockToChain(), appendItemToChain(), appendLocaleToChain(), baseCompile(), baseCompile$1(), clearCompileCache(), compile(), compileMessageFormat() (+88 more)

### Community 49 - "Community 49"
Cohesion: 0.03
Nodes (75): addSub(), apply(), BaseReactiveHandler, batch(), checkIdentityKeys(), cleanupDeps(), cleanupEffect(), ComputedRefImpl (+67 more)

### Community 50 - "Community 50"
Cohesion: 0.03
Nodes (75): addSub(), apply(), BaseReactiveHandler, batch(), checkIdentityKeys(), cleanupDeps(), cleanupEffect(), ComputedRefImpl (+67 more)

### Community 51 - "Community 51"
Cohesion: 0.03
Nodes (71): addSub(), apply(), BaseReactiveHandler, batch(), cleanupDeps(), cleanupEffect(), ComputedRefImpl, createInstrumentationGetter() (+63 more)

### Community 52 - "Community 52"
Cohesion: 0.03
Nodes (50): analyzeImportedModDifference(), binarySearch(), CallSiteToString(), cleanUrl(), cloneCallSite(), createHMRHandler(), decode(), DecodedMap (+42 more)

### Community 53 - "Community 53"
Cohesion: 0.04
Nodes (93): adjustI18nResources(), appendBlockToChain(), appendItemToChain(), appendLocaleToChain(), apply(), clearDateTimeFormat(), clearNumberFormat(), compileMessageFormat() (+85 more)

### Community 54 - "Community 54"
Cohesion: 0.05
Nodes (94): c(), e$(), e1(), e7(), e8(), e9(), eA(), eb() (+86 more)

### Community 55 - "Community 55"
Cohesion: 0.04
Nodes (15): BitSet, Bundle, Chunk, decode(), encode(), encodeInteger(), flush(), getLocator() (+7 more)

### Community 56 - "Community 56"
Cohesion: 0.06
Nodes (84): c(), d(), e_(), e1(), e2(), e4(), e5(), e6() (+76 more)

### Community 57 - "Community 57"
Cohesion: 0.04
Nodes (10): BitSet, Bundle, Chunk, getLocator(), getRelativePath(), guessIndent(), isObject(), MagicString (+2 more)

### Community 58 - "Community 58"
Cohesion: 0.05
Nodes (46): A(), B(), c(), d(), E(), e7(), e9(), ea (+38 more)

### Community 59 - "Community 59"
Cohesion: 0.03
Nodes (41): addEventListener(), autoPrefix(), callModelHook(), createInvoker(), getCheckboxValue(), getNow(), getPosition(), getTimeout() (+33 more)

### Community 60 - "Community 60"
Cohesion: 0.03
Nodes (39): addEventListener(), autoPrefix(), callModelHook(), createInvoker(), getCheckboxValue(), getNow(), getPosition(), getTimeout() (+31 more)

### Community 61 - "Community 61"
Cohesion: 0.03
Nodes (38): addEventListener(), autoPrefix(), callModelHook(), createInvoker(), getCheckboxValue(), getNow(), getPosition(), getTimeout() (+30 more)

### Community 62 - "Community 62"
Cohesion: 0.06
Nodes (69): a(), an(), at(), b(), be(), bt(), c(), constructor() (+61 more)

### Community 63 - "Community 63"
Cohesion: 0.06
Nodes (39): a(), b(), d, E(), ea(), eb(), eC, eD() (+31 more)

### Community 64 - "Community 64"
Cohesion: 0.1
Nodes (59): a(), an(), B(), bt(), c(), d(), dt(), E() (+51 more)

### Community 65 - "Community 65"
Cohesion: 0.05
Nodes (33): arrayOf(), arrayOfType(), assertEach(), assertNodeType(), assertValueType(), chain(), copy(), defineType() (+25 more)

### Community 66 - "Community 66"
Cohesion: 0.05
Nodes (39): actionGlobalCopyState(), actionGlobalOpenStateFile(), actionGlobalPasteState(), actionGlobalSaveState(), addStoreToDevtools(), ApiProxy, bom(), checkClipboardAccess() (+31 more)

### Community 67 - "Community 67"
Cohesion: 0.07
Nodes (34): b2n(), b2p(), calln(), Color, eq(), from(), fromObject(), functionParse() (+26 more)

### Community 68 - "Community 68"
Cohesion: 0.14
Nodes (44): ae(), B(), be(), c(), d(), de(), E(), ee() (+36 more)

### Community 69 - "Community 69"
Cohesion: 0.11
Nodes (46): a(), ae(), B(), c(), ce(), ct(), D(), E() (+38 more)

### Community 70 - "Community 70"
Cohesion: 0.06
Nodes (32): actionGlobalCopyState(), actionGlobalOpenStateFile(), actionGlobalPasteState(), actionGlobalSaveState(), addStoreToDevtools(), bom(), checkClipboardAccess(), checkNotFocusedError() (+24 more)

### Community 71 - "Community 71"
Cohesion: 0.07
Nodes (25): isDate(), isFunction(), isIntegerKey(), isMap(), isObject(), isPlainObject(), isPromise(), isRef() (+17 more)

### Community 72 - "Community 72"
Cohesion: 0.07
Nodes (25): isDate(), isFunction(), isIntegerKey(), isMap(), isObject(), isPlainObject(), isPromise(), isRef() (+17 more)

### Community 73 - "Community 73"
Cohesion: 0.07
Nodes (25): isDate(), isFunction(), isIntegerKey(), isMap(), isObject(), isPlainObject(), isPromise(), isRef() (+17 more)

### Community 74 - "Community 74"
Cohesion: 0.08
Nodes (47): Exception, analyze_strip(), _assign_pads_by_column(), _cluster_rows(), CVDetectionError, debug_analyze_strip(), _detect_orientation(), _enforce_pad_x_consistency() (+39 more)

### Community 75 - "Community 75"
Cohesion: 0.1
Nodes (40): buildSSRProps(), clone(), compile(), createChildContext(), createSSRCompilerError(), createSSRTransformContext(), createVNodeSlotBranch(), filterChild() (+32 more)

### Community 76 - "Community 76"
Cohesion: 0.1
Nodes (19): a(), d(), e(), f(), h(), l(), m(), n() (+11 more)

### Community 77 - "Community 77"
Cohesion: 0.09
Nodes (35): applySSRDirectives(), createBuffer(), isComment(), nestedUnrollBuffer(), pipeToNodeWritable(), pipeToWebWritable(), renderComponentSubTree(), renderComponentVNode() (+27 more)

### Community 78 - "Community 78"
Cohesion: 0.09
Nodes (35): applySSRDirectives(), createBuffer(), isComment(), nestedUnrollBuffer(), pipeToNodeWritable(), pipeToWebWritable(), renderComponentSubTree(), renderComponentVNode() (+27 more)

### Community 79 - "Community 79"
Cohesion: 0.09
Nodes (35): applySSRDirectives(), createBuffer(), isComment(), nestedUnrollBuffer(), pipeToNodeWritable(), pipeToWebWritable(), renderComponentSubTree(), renderComponentVNode() (+27 more)

### Community 80 - "Community 80"
Cohesion: 0.07
Nodes (5): cloneNode(), formatArgs(), getDate(), Node, sourceOffset()

### Community 81 - "Community 81"
Cohesion: 0.09
Nodes (21): create(), deepCopy(), format(), friendlyJSONstringify(), generateCodeFrame(), generateFormatCacheKey(), getGlobalThis(), isDate() (+13 more)

### Community 82 - "Community 82"
Cohesion: 0.09
Nodes (20): create(), deepCopy(), format(), friendlyJSONstringify(), generateCodeFrame(), generateFormatCacheKey(), getGlobalThis(), isDate() (+12 more)

### Community 83 - "Community 83"
Cohesion: 0.12
Nodes (24): baseCompile(), createCodeGenerator(), createCompileError(), createCompileWarn(), createParser(), createScanner(), createTokenizer(), createTransformer() (+16 more)

### Community 84 - "Community 84"
Cohesion: 0.12
Nodes (24): baseCompile(), createCodeGenerator(), createCompileError(), createCompileWarn(), createParser(), createScanner(), createTokenizer(), createTransformer() (+16 more)

### Community 85 - "Community 85"
Cohesion: 0.15
Nodes (5): cleanMarks(), getEvents(), isPromise(), LazyResult, toStack()

### Community 86 - "Community 86"
Cohesion: 0.12
Nodes (20): baseCompile(), createCodeGenerator(), createParser(), createScanner(), createTokenizer(), createTransformer(), generate(), generateLinkedNode() (+12 more)

### Community 87 - "Community 87"
Cohesion: 0.09
Nodes (6): AxiosHeaders, isValidHeaderName(), matchHeaderValue(), normalizeHeader(), parseTokens(), set()

### Community 88 - "Community 88"
Cohesion: 0.15
Nodes (6): atruleStart(), capitalize(), escapeHTMLInCSS(), pushBlock(), pushBody(), Stringifier

### Community 89 - "Community 89"
Cohesion: 0.13
Nodes (3): cleanSource(), Container, markTreeDirty()

### Community 90 - "Community 90"
Cohesion: 0.11
Nodes (10): createWatchHooks(), dateTime(), Emitter, extractWatchHooks(), processOk(), SignalExit, SignalExitBase, SignalExitFallback (+2 more)

### Community 91 - "Community 91"
Cohesion: 0.12
Nodes (14): analyzeNode(), createDOMCompilerError(), evaluateConstant(), getCachedNode(), ignoreSideEffectTags(), isValidHTMLNesting(), stringifyElement(), stringifyNode() (+6 more)

### Community 92 - "Community 92"
Cohesion: 0.1
Nodes (6): catchupLine(), encodeGeneratedRanges(), decode(), sort(), StringReader, StringWriter

### Community 93 - "Community 93"
Cohesion: 0.16
Nodes (21): addCommandPluginsToInputOptions(), addPluginsFromCommandOption(), batchWarnings(), defaultBody(), formatLocation(), generateLogFilter(), getCamelizedPluginBaseName(), getConfigFileExport() (+13 more)

### Community 94 - "Community 94"
Cohesion: 0.18
Nodes (7): determineBranch(), EntityDecoder, getDecoder(), isAsciiAlphaNumeric(), isEntityInAttributeInvalidEnd(), isHexadecimalCharacter(), isNumber()

### Community 95 - "Community 95"
Cohesion: 0.14
Nodes (11): analyzeNode(), createDOMCompilerError(), evaluateConstant(), getCachedNode(), stringifyElement(), stringifyNode(), stringifyStatic(), transformModel() (+3 more)

### Community 96 - "Community 96"
Cohesion: 0.25
Nodes (1): MapGenerator

### Community 97 - "Community 97"
Cohesion: 0.23
Nodes (16): catchupLine(), decode(), decodeGeneratedRanges(), decodeInteger(), decodeOriginalScopes(), encode(), encodeGeneratedRanges(), encodeInteger() (+8 more)

### Community 98 - "Community 98"
Cohesion: 0.14
Nodes (8): createDOMCompilerError(), ignoreSideEffectTags(), isValidHTMLNesting(), transformModel(), transformShow(), transformVHtml(), transformVText(), validateHtmlNesting()

### Community 99 - "Community 99"
Cohesion: 0.14
Nodes (1): NoWorkResult

### Community 100 - "Community 100"
Cohesion: 0.26
Nodes (12): a(), c(), D(), E(), m(), n(), o(), P() (+4 more)

### Community 101 - "Community 101"
Cohesion: 0.18
Nodes (5): isProcessableURL(), isValid(), loadImportContent(), parseStyles$1(), resolveImportId()

### Community 102 - "Community 102"
Cohesion: 0.18
Nodes (10): async_setup_entry(), FluvalChannelNumber, Number entities for each Fluval RGBW channel., NumberEntity, build_set_channels_command(), build_single_channel_command(), Fluval Shaker BLE protocol implementation., Build the BLE write payload for setting all channels simultaneously.     r, g, (+2 more)

### Community 103 - "Community 103"
Cohesion: 0.23
Nodes (8): beforeCreate(), d(), get(), i(), o(), p(), set(), v()

### Community 104 - "Community 104"
Cohesion: 0.25
Nodes (3): fromBase64(), PreviousMap, realPath()

### Community 105 - "Community 105"
Cohesion: 0.28
Nodes (11): applyManualBinaryPathOverride(), checkAndPreparePackage(), downloadDirectlyFromNPM(), downloadedBinPath(), extractFileFromTarGzip(), fetch(), installUsingNPM(), isYarn() (+3 more)

### Community 106 - "Community 106"
Cohesion: 0.24
Nodes (5): asyncWalk(), AsyncWalker, SyncWalker, walk(), WalkerBase

### Community 107 - "Community 107"
Cohesion: 0.32
Nodes (11): base64Bytes(), estimateBase64BufferAllocation(), estimateDataURLBufferAllocation(), estimateDataURLBytes(), estimateDataURLDecodedBytes(), estimatePercentDecodedBase64Bytes(), hexValue(), isBase64Char() (+3 more)

### Community 108 - "Community 108"
Cohesion: 0.29
Nodes (9): isIPv4Loopback(), isIPv6Loopback(), isIPv6Unspecified(), isLoopback(), normalizeIPAddress(), normalizeNoProxyHost(), parseIPv4Octet(), shouldBypassProxy() (+1 more)

### Community 109 - "Community 109"
Cohesion: 0.26
Nodes (1): WatchEmitter

### Community 110 - "Community 110"
Cohesion: 0.27
Nodes (10): find_db(), main(), migrate_calendar_tasks(), migrate_dosing_tasks(), migrate_fish(), migrate_supplies(), Insert supplies that do not already exist (checked by name).     Returns a mapp, Insert dosing tasks linked to the new supplies.     Skips silently if a dosing (+2 more)

### Community 111 - "Community 111"
Cohesion: 0.29
Nodes (2): getLineToIndex(), Input

### Community 112 - "Community 112"
Cohesion: 0.31
Nodes (4): classMethodOrDeclareMethodCommon(), classMethodOrPropertyCommon(), functionCommon(), functionDeclarationCommon()

### Community 113 - "Community 113"
Cohesion: 0.28
Nodes (3): aggregateErrorMessage(), AxiosError, redactConfig()

### Community 114 - "Community 114"
Cohesion: 0.36
Nodes (6): fetch_wikipedia_image(), main(), _query_wiki(), Try full latin, then genus+species (skipping cf./sp./var.), then genus only., isPerformanceSupported(), now()

### Community 115 - "Community 115"
Cohesion: 0.29
Nodes (1): CancelToken

### Community 116 - "Community 116"
Cohesion: 0.38
Nodes (3): factory(), getFetch(), test()

### Community 117 - "Community 117"
Cohesion: 0.52
Nodes (6): assertValidHttpProtocolURL(), buildFullPath(), normalizeURLForProtocolCheck(), redactFragment(), redactSensitiveURLParts(), stripLeadingC0ControlOrSpace()

### Community 118 - "Community 118"
Cohesion: 0.29
Nodes (1): InterceptorManager

### Community 119 - "Community 119"
Cohesion: 0.29
Nodes (1): Result

### Community 120 - "Community 120"
Cohesion: 0.48
Nodes (5): getPackageBase(), getReportHeader(), isMingw32(), isMusl(), throwUnsupportedError()

### Community 121 - "Community 121"
Cohesion: 0.4
Nodes (3): FluvalBLEConfigFlow, Config flow for Fluval Shaker BLE., Handle Bluetooth discovery — auto-populate MAC.

### Community 122 - "Community 122"
Cohesion: 0.53
Nodes (4): isReservedWord(), isStrictBindOnlyReservedWord(), isStrictBindReservedWord(), isStrictReservedWord()

### Community 123 - "Community 123"
Cohesion: 0.67
Nodes (5): cloneIfNode(), cloneIfNodeOrArray(), cloneNode(), cloneNodeInternal(), maybeCloneComments()

### Community 124 - "Community 124"
Cohesion: 0.33
Nodes (0): 

### Community 125 - "Community 125"
Cohesion: 0.53
Nodes (4): sanitizeByteStringHeaderValue(), sanitizeHeaderValue(), sanitizeValue(), trimSPorHTAB()

### Community 126 - "Community 126"
Cohesion: 0.4
Nodes (2): removeBrackets(), renderKey()

### Community 127 - "Community 127"
Cohesion: 0.33
Nodes (0): 

### Community 128 - "Community 128"
Cohesion: 0.47
Nodes (1): CssSyntaxError

### Community 129 - "Community 129"
Cohesion: 0.47
Nodes (1): Processor

### Community 130 - "Community 130"
Cohesion: 0.33
Nodes (1): Root

### Community 131 - "Community 131"
Cohesion: 0.4
Nodes (2): nextToken(), unclosed()

### Community 132 - "Community 132"
Cohesion: 0.33
Nodes (0): 

### Community 133 - "Community 133"
Cohesion: 0.8
Nodes (4): isIdentifierChar(), isIdentifierName(), isIdentifierStart(), isInAstralSet()

### Community 134 - "Community 134"
Cohesion: 0.7
Nodes (4): validate(), validateChild(), validateField(), validateInternal()

### Community 135 - "Community 135"
Cohesion: 0.4
Nodes (4): ComputedRefImpl, EffectScope, ReactiveEffect, ShallowReactiveBrandClass

### Community 136 - "Community 136"
Cohesion: 0.4
Nodes (0): 

### Community 137 - "Community 137"
Cohesion: 0.5
Nodes (2): parsePropPath(), throwIfDepthExceeded()

### Community 138 - "Community 138"
Cohesion: 0.4
Nodes (1): AsyncWalker

### Community 139 - "Community 139"
Cohesion: 0.4
Nodes (1): WalkerBase

### Community 140 - "Community 140"
Cohesion: 0.5
Nodes (2): customAlphabet(), customRandom()

### Community 141 - "Community 141"
Cohesion: 0.4
Nodes (1): AtRule

### Community 142 - "Community 142"
Cohesion: 0.5
Nodes (2): stringify$1(), stringifyNode()

### Community 143 - "Community 143"
Cohesion: 0.4
Nodes (4): DecodedMap, HMRClient, HMRMessenger, ModuleCacheMap

### Community 144 - "Community 144"
Cohesion: 0.67
Nodes (3): _commons_images(), Species image and metadata search — Wikipedia summary + Wikimedia Commons fallba, search_species()

### Community 145 - "Community 145"
Cohesion: 0.83
Nodes (3): isPlainObject(), isRegExp(), valueToNode()

### Community 146 - "Community 146"
Cohesion: 0.83
Nodes (3): getFunctionName(), getNameFromLiteralId(), getObjectMemberKey()

### Community 147 - "Community 147"
Cohesion: 0.5
Nodes (1): ApiProxy

### Community 148 - "Community 148"
Cohesion: 0.67
Nodes (2): ascending(), descending()

### Community 149 - "Community 149"
Cohesion: 0.83
Nodes (3): getAdapter(), isResolvedHandle(), renderReason()

### Community 150 - "Community 150"
Cohesion: 0.67
Nodes (2): mergeConfig(), ownEnumerableKeys()

### Community 151 - "Community 151"
Cohesion: 0.67
Nodes (2): remove(), write()

### Community 152 - "Community 152"
Cohesion: 0.5
Nodes (0): 

### Community 153 - "Community 153"
Cohesion: 0.5
Nodes (3): Animation, Animations, Animator

### Community 154 - "Community 154"
Cohesion: 0.83
Nodes (3): encodeHTML(), encodeHTMLTrieRe(), encodeNonAsciiHTML()

### Community 155 - "Community 155"
Cohesion: 0.5
Nodes (1): SyncWalker

### Community 156 - "Community 156"
Cohesion: 0.5
Nodes (0): 

### Community 157 - "Community 157"
Cohesion: 0.5
Nodes (3): Bundle, MagicString, SourceMap

### Community 158 - "Community 158"
Cohesion: 0.5
Nodes (0): 

### Community 159 - "Community 159"
Cohesion: 0.5
Nodes (1): Declaration

### Community 160 - "Community 160"
Cohesion: 0.5
Nodes (1): Document

### Community 161 - "Community 161"
Cohesion: 0.83
Nodes (3): constructNode(), fromJSON(), hydrateInputs()

### Community 162 - "Community 162"
Cohesion: 0.5
Nodes (1): Rule

### Community 163 - "Community 163"
Cohesion: 0.67
Nodes (2): getTokenType(), terminalHighlight()

### Community 164 - "Community 164"
Cohesion: 0.5
Nodes (1): Warning

### Community 165 - "Community 165"
Cohesion: 0.5
Nodes (0): 

### Community 166 - "Community 166"
Cohesion: 0.5
Nodes (3): SourceMapConsumer, SourceMapGenerator, SourceNode

### Community 167 - "Community 167"
Cohesion: 1.0
Nodes (2): getQualifiedName(), removeTypeDuplicates()

### Community 168 - "Community 168"
Cohesion: 1.0
Nodes (2): traverse(), traverseSimpleImpl()

### Community 169 - "Community 169"
Cohesion: 1.0
Nodes (2): captureShortStackTrace(), deprecationWarning()

### Community 170 - "Community 170"
Cohesion: 1.0
Nodes (2): isMemberExpressionLike(), matchesPattern()

### Community 171 - "Community 171"
Cohesion: 1.0
Nodes (2): getDevtoolsGlobalHook(), getTarget()

### Community 172 - "Community 172"
Cohesion: 0.67
Nodes (0): 

### Community 173 - "Community 173"
Cohesion: 1.0
Nodes (2): iterate(), runJob()

### Community 174 - "Community 174"
Cohesion: 1.0
Nodes (2): done(), onloadend()

### Community 175 - "Community 175"
Cohesion: 0.67
Nodes (1): CanceledError

### Community 176 - "Community 176"
Cohesion: 1.0
Nodes (2): dispatchRequest(), throwIfCancellationRequested()

### Community 177 - "Community 177"
Cohesion: 0.67
Nodes (0): 

### Community 178 - "Community 178"
Cohesion: 0.67
Nodes (0): 

### Community 179 - "Community 179"
Cohesion: 1.0
Nodes (2): encodeUTF8(), resolveConfig()

### Community 180 - "Community 180"
Cohesion: 0.67
Nodes (0): 

### Community 181 - "Community 181"
Cohesion: 1.0
Nodes (2): decodeCodePoint(), replaceCodePoint()

### Community 182 - "Community 182"
Cohesion: 0.67
Nodes (0): 

### Community 183 - "Community 183"
Cohesion: 0.67
Nodes (0): 

### Community 184 - "Community 184"
Cohesion: 0.67
Nodes (1): Comment

### Community 185 - "Community 185"
Cohesion: 0.67
Nodes (0): 

### Community 186 - "Community 186"
Cohesion: 0.67
Nodes (0): 

### Community 187 - "Community 187"
Cohesion: 0.67
Nodes (0): 

### Community 188 - "Community 188"
Cohesion: 0.67
Nodes (0): 

### Community 189 - "Community 189"
Cohesion: 0.67
Nodes (0): 

### Community 190 - "Community 190"
Cohesion: 0.67
Nodes (2): ESModulesRunner, ViteRuntime

### Community 191 - "Community 191"
Cohesion: 0.67
Nodes (0): 

### Community 192 - "Community 192"
Cohesion: 0.67
Nodes (0): 

### Community 193 - "Community 193"
Cohesion: 0.67
Nodes (0): 

### Community 194 - "Community 194"
Cohesion: 0.67
Nodes (0): 

### Community 195 - "Community 195"
Cohesion: 1.0
Nodes (1): Fluval Shaker RGBW BLE custom component for Home Assistant.  Extends mrzottel/

### Community 196 - "Community 196"
Cohesion: 1.0
Nodes (1): Position

### Community 197 - "Community 197"
Cohesion: 1.0
Nodes (0): 

### Community 198 - "Community 198"
Cohesion: 1.0
Nodes (0): 

### Community 199 - "Community 199"
Cohesion: 1.0
Nodes (0): 

### Community 200 - "Community 200"
Cohesion: 1.0
Nodes (0): 

### Community 201 - "Community 201"
Cohesion: 1.0
Nodes (0): 

### Community 202 - "Community 202"
Cohesion: 1.0
Nodes (0): 

### Community 203 - "Community 203"
Cohesion: 1.0
Nodes (0): 

### Community 204 - "Community 204"
Cohesion: 1.0
Nodes (0): 

### Community 205 - "Community 205"
Cohesion: 1.0
Nodes (0): 

### Community 206 - "Community 206"
Cohesion: 1.0
Nodes (0): 

### Community 207 - "Community 207"
Cohesion: 1.0
Nodes (0): 

### Community 208 - "Community 208"
Cohesion: 1.0
Nodes (0): 

### Community 209 - "Community 209"
Cohesion: 1.0
Nodes (0): 

### Community 210 - "Community 210"
Cohesion: 1.0
Nodes (0): 

### Community 211 - "Community 211"
Cohesion: 1.0
Nodes (0): 

### Community 212 - "Community 212"
Cohesion: 1.0
Nodes (0): 

### Community 213 - "Community 213"
Cohesion: 1.0
Nodes (0): 

### Community 214 - "Community 214"
Cohesion: 1.0
Nodes (0): 

### Community 215 - "Community 215"
Cohesion: 1.0
Nodes (0): 

### Community 216 - "Community 216"
Cohesion: 1.0
Nodes (0): 

### Community 217 - "Community 217"
Cohesion: 1.0
Nodes (0): 

### Community 218 - "Community 218"
Cohesion: 1.0
Nodes (0): 

### Community 219 - "Community 219"
Cohesion: 1.0
Nodes (0): 

### Community 220 - "Community 220"
Cohesion: 1.0
Nodes (0): 

### Community 221 - "Community 221"
Cohesion: 1.0
Nodes (0): 

### Community 222 - "Community 222"
Cohesion: 1.0
Nodes (0): 

### Community 223 - "Community 223"
Cohesion: 1.0
Nodes (0): 

### Community 224 - "Community 224"
Cohesion: 1.0
Nodes (0): 

### Community 225 - "Community 225"
Cohesion: 1.0
Nodes (0): 

### Community 226 - "Community 226"
Cohesion: 1.0
Nodes (0): 

### Community 227 - "Community 227"
Cohesion: 1.0
Nodes (0): 

### Community 228 - "Community 228"
Cohesion: 1.0
Nodes (0): 

### Community 229 - "Community 229"
Cohesion: 1.0
Nodes (0): 

### Community 230 - "Community 230"
Cohesion: 1.0
Nodes (0): 

### Community 231 - "Community 231"
Cohesion: 1.0
Nodes (0): 

### Community 232 - "Community 232"
Cohesion: 1.0
Nodes (0): 

### Community 233 - "Community 233"
Cohesion: 1.0
Nodes (0): 

### Community 234 - "Community 234"
Cohesion: 1.0
Nodes (0): 

### Community 235 - "Community 235"
Cohesion: 1.0
Nodes (0): 

### Community 236 - "Community 236"
Cohesion: 1.0
Nodes (0): 

### Community 237 - "Community 237"
Cohesion: 1.0
Nodes (0): 

### Community 238 - "Community 238"
Cohesion: 1.0
Nodes (0): 

### Community 239 - "Community 239"
Cohesion: 1.0
Nodes (0): 

### Community 240 - "Community 240"
Cohesion: 1.0
Nodes (0): 

### Community 241 - "Community 241"
Cohesion: 1.0
Nodes (0): 

### Community 242 - "Community 242"
Cohesion: 1.0
Nodes (0): 

### Community 243 - "Community 243"
Cohesion: 1.0
Nodes (0): 

### Community 244 - "Community 244"
Cohesion: 1.0
Nodes (0): 

### Community 245 - "Community 245"
Cohesion: 1.0
Nodes (0): 

### Community 246 - "Community 246"
Cohesion: 1.0
Nodes (0): 

### Community 247 - "Community 247"
Cohesion: 1.0
Nodes (0): 

### Community 248 - "Community 248"
Cohesion: 1.0
Nodes (0): 

### Community 249 - "Community 249"
Cohesion: 1.0
Nodes (0): 

### Community 250 - "Community 250"
Cohesion: 1.0
Nodes (0): 

### Community 251 - "Community 251"
Cohesion: 1.0
Nodes (0): 

### Community 252 - "Community 252"
Cohesion: 1.0
Nodes (0): 

### Community 253 - "Community 253"
Cohesion: 1.0
Nodes (0): 

### Community 254 - "Community 254"
Cohesion: 1.0
Nodes (0): 

### Community 255 - "Community 255"
Cohesion: 1.0
Nodes (0): 

### Community 256 - "Community 256"
Cohesion: 1.0
Nodes (1): Color

### Community 257 - "Community 257"
Cohesion: 1.0
Nodes (1): ApiProxy

### Community 258 - "Community 258"
Cohesion: 1.0
Nodes (1): VueElement

### Community 259 - "Community 259"
Cohesion: 1.0
Nodes (0): 

### Community 260 - "Community 260"
Cohesion: 1.0
Nodes (0): 

### Community 261 - "Community 261"
Cohesion: 1.0
Nodes (0): 

### Community 262 - "Community 262"
Cohesion: 1.0
Nodes (0): 

### Community 263 - "Community 263"
Cohesion: 1.0
Nodes (0): 

### Community 264 - "Community 264"
Cohesion: 1.0
Nodes (0): 

### Community 265 - "Community 265"
Cohesion: 1.0
Nodes (0): 

### Community 266 - "Community 266"
Cohesion: 1.0
Nodes (0): 

### Community 267 - "Community 267"
Cohesion: 1.0
Nodes (0): 

### Community 268 - "Community 268"
Cohesion: 1.0
Nodes (0): 

### Community 269 - "Community 269"
Cohesion: 1.0
Nodes (0): 

### Community 270 - "Community 270"
Cohesion: 1.0
Nodes (0): 

### Community 271 - "Community 271"
Cohesion: 1.0
Nodes (0): 

### Community 272 - "Community 272"
Cohesion: 1.0
Nodes (0): 

### Community 273 - "Community 273"
Cohesion: 1.0
Nodes (0): 

### Community 274 - "Community 274"
Cohesion: 1.0
Nodes (0): 

### Community 275 - "Community 275"
Cohesion: 1.0
Nodes (0): 

### Community 276 - "Community 276"
Cohesion: 1.0
Nodes (0): 

### Community 277 - "Community 277"
Cohesion: 1.0
Nodes (0): 

### Community 278 - "Community 278"
Cohesion: 1.0
Nodes (0): 

### Community 279 - "Community 279"
Cohesion: 1.0
Nodes (0): 

### Community 280 - "Community 280"
Cohesion: 1.0
Nodes (0): 

### Community 281 - "Community 281"
Cohesion: 1.0
Nodes (0): 

### Community 282 - "Community 282"
Cohesion: 1.0
Nodes (0): 

### Community 283 - "Community 283"
Cohesion: 1.0
Nodes (0): 

### Community 284 - "Community 284"
Cohesion: 1.0
Nodes (0): 

### Community 285 - "Community 285"
Cohesion: 1.0
Nodes (0): 

### Community 286 - "Community 286"
Cohesion: 1.0
Nodes (1): BarController

### Community 287 - "Community 287"
Cohesion: 1.0
Nodes (1): BubbleController

### Community 288 - "Community 288"
Cohesion: 1.0
Nodes (1): DoughnutController

### Community 289 - "Community 289"
Cohesion: 1.0
Nodes (1): LineController

### Community 290 - "Community 290"
Cohesion: 1.0
Nodes (1): PieController

### Community 291 - "Community 291"
Cohesion: 1.0
Nodes (1): PolarAreaController

### Community 292 - "Community 292"
Cohesion: 1.0
Nodes (1): RadarController

### Community 293 - "Community 293"
Cohesion: 1.0
Nodes (1): ScatterController

### Community 294 - "Community 294"
Cohesion: 1.0
Nodes (1): Animation

### Community 295 - "Community 295"
Cohesion: 1.0
Nodes (1): Animations

### Community 296 - "Community 296"
Cohesion: 1.0
Nodes (1): Animator

### Community 297 - "Community 297"
Cohesion: 1.0
Nodes (1): Config

### Community 298 - "Community 298"
Cohesion: 1.0
Nodes (1): Chart

### Community 299 - "Community 299"
Cohesion: 1.0
Nodes (1): DatasetController

### Community 300 - "Community 300"
Cohesion: 1.0
Nodes (1): Defaults

### Community 301 - "Community 301"
Cohesion: 1.0
Nodes (1): Element

### Community 302 - "Community 302"
Cohesion: 1.0
Nodes (1): PluginService

### Community 303 - "Community 303"
Cohesion: 1.0
Nodes (1): Registry

### Community 304 - "Community 304"
Cohesion: 1.0
Nodes (1): TypedRegistry

### Community 305 - "Community 305"
Cohesion: 1.0
Nodes (1): ArcElement

### Community 306 - "Community 306"
Cohesion: 1.0
Nodes (1): BarElement

### Community 307 - "Community 307"
Cohesion: 1.0
Nodes (1): PointElement

### Community 308 - "Community 308"
Cohesion: 1.0
Nodes (1): BasePlatform

### Community 309 - "Community 309"
Cohesion: 1.0
Nodes (1): BasicPlatform

### Community 310 - "Community 310"
Cohesion: 1.0
Nodes (1): DomPlatform

### Community 311 - "Community 311"
Cohesion: 1.0
Nodes (1): simpleArc

### Community 312 - "Community 312"
Cohesion: 1.0
Nodes (0): 

### Community 313 - "Community 313"
Cohesion: 1.0
Nodes (0): 

### Community 314 - "Community 314"
Cohesion: 1.0
Nodes (1): Tooltip

### Community 315 - "Community 315"
Cohesion: 1.0
Nodes (1): CategoryScale

### Community 316 - "Community 316"
Cohesion: 1.0
Nodes (1): LinearScale

### Community 317 - "Community 317"
Cohesion: 1.0
Nodes (1): LinearScaleBase

### Community 318 - "Community 318"
Cohesion: 1.0
Nodes (1): LogarithmicScale

### Community 319 - "Community 319"
Cohesion: 1.0
Nodes (1): RadialLinearScale

### Community 320 - "Community 320"
Cohesion: 1.0
Nodes (1): TimeScale

### Community 321 - "Community 321"
Cohesion: 1.0
Nodes (1): TimeSeriesScale

### Community 322 - "Community 322"
Cohesion: 1.0
Nodes (0): 

### Community 323 - "Community 323"
Cohesion: 1.0
Nodes (0): 

### Community 324 - "Community 324"
Cohesion: 1.0
Nodes (0): 

### Community 325 - "Community 325"
Cohesion: 1.0
Nodes (1): EntityDecoder

### Community 326 - "Community 326"
Cohesion: 1.0
Nodes (0): 

### Community 327 - "Community 327"
Cohesion: 1.0
Nodes (0): 

### Community 328 - "Community 328"
Cohesion: 1.0
Nodes (1): AsyncWalker

### Community 329 - "Community 329"
Cohesion: 1.0
Nodes (1): SyncWalker

### Community 330 - "Community 330"
Cohesion: 1.0
Nodes (1): WalkerBase

### Community 331 - "Community 331"
Cohesion: 1.0
Nodes (1): HttpsProxyAgent

### Community 332 - "Community 332"
Cohesion: 1.0
Nodes (0): 

### Community 333 - "Community 333"
Cohesion: 1.0
Nodes (0): 

### Community 334 - "Community 334"
Cohesion: 1.0
Nodes (1): AtRule_

### Community 335 - "Community 335"
Cohesion: 1.0
Nodes (1): Comment_

### Community 336 - "Community 336"
Cohesion: 1.0
Nodes (1): Container

### Community 337 - "Community 337"
Cohesion: 1.0
Nodes (1): CssSyntaxError_

### Community 338 - "Community 338"
Cohesion: 1.0
Nodes (1): Declaration_

### Community 339 - "Community 339"
Cohesion: 1.0
Nodes (1): Document_

### Community 340 - "Community 340"
Cohesion: 1.0
Nodes (1): Input_

### Community 341 - "Community 341"
Cohesion: 1.0
Nodes (1): LazyResult_

### Community 342 - "Community 342"
Cohesion: 1.0
Nodes (1): NoWorkResult_

### Community 343 - "Community 343"
Cohesion: 1.0
Nodes (1): Node

### Community 344 - "Community 344"
Cohesion: 1.0
Nodes (0): 

### Community 345 - "Community 345"
Cohesion: 1.0
Nodes (1): PreviousMap_

### Community 346 - "Community 346"
Cohesion: 1.0
Nodes (1): Processor_

### Community 347 - "Community 347"
Cohesion: 1.0
Nodes (1): Result_

### Community 348 - "Community 348"
Cohesion: 1.0
Nodes (1): Root_

### Community 349 - "Community 349"
Cohesion: 1.0
Nodes (1): Rule_

### Community 350 - "Community 350"
Cohesion: 1.0
Nodes (1): Stringifier_

### Community 351 - "Community 351"
Cohesion: 1.0
Nodes (0): 

### Community 352 - "Community 352"
Cohesion: 1.0
Nodes (1): Warning_

### Community 353 - "Community 353"
Cohesion: 1.0
Nodes (0): 

### Community 354 - "Community 354"
Cohesion: 1.0
Nodes (0): 

### Community 355 - "Community 355"
Cohesion: 1.0
Nodes (0): 

### Community 356 - "Community 356"
Cohesion: 1.0
Nodes (0): 

### Community 357 - "Community 357"
Cohesion: 1.0
Nodes (0): 

### Community 358 - "Community 358"
Cohesion: 1.0
Nodes (0): 

### Community 359 - "Community 359"
Cohesion: 1.0
Nodes (0): 

### Community 360 - "Community 360"
Cohesion: 1.0
Nodes (0): 

### Community 361 - "Community 361"
Cohesion: 1.0
Nodes (0): 

### Community 362 - "Community 362"
Cohesion: 1.0
Nodes (0): 

### Community 363 - "Community 363"
Cohesion: 1.0
Nodes (0): 

### Community 364 - "Community 364"
Cohesion: 1.0
Nodes (0): 

### Community 365 - "Community 365"
Cohesion: 1.0
Nodes (0): 

### Community 366 - "Community 366"
Cohesion: 1.0
Nodes (0): 

### Community 367 - "Community 367"
Cohesion: 1.0
Nodes (0): 

### Community 368 - "Community 368"
Cohesion: 1.0
Nodes (0): 

### Community 369 - "Community 369"
Cohesion: 1.0
Nodes (0): 

### Community 370 - "Community 370"
Cohesion: 1.0
Nodes (0): 

### Community 371 - "Community 371"
Cohesion: 1.0
Nodes (0): 

### Community 372 - "Community 372"
Cohesion: 1.0
Nodes (0): 

### Community 373 - "Community 373"
Cohesion: 1.0
Nodes (0): 

### Community 374 - "Community 374"
Cohesion: 1.0
Nodes (0): 

### Community 375 - "Community 375"
Cohesion: 1.0
Nodes (0): 

### Community 376 - "Community 376"
Cohesion: 1.0
Nodes (0): 

### Community 377 - "Community 377"
Cohesion: 1.0
Nodes (0): 

### Community 378 - "Community 378"
Cohesion: 1.0
Nodes (0): 

### Community 379 - "Community 379"
Cohesion: 1.0
Nodes (0): 

### Community 380 - "Community 380"
Cohesion: 1.0
Nodes (0): 

### Community 381 - "Community 381"
Cohesion: 1.0
Nodes (0): 

### Community 382 - "Community 382"
Cohesion: 1.0
Nodes (0): 

### Community 383 - "Community 383"
Cohesion: 1.0
Nodes (0): 

### Community 384 - "Community 384"
Cohesion: 1.0
Nodes (0): 

### Community 385 - "Community 385"
Cohesion: 1.0
Nodes (0): 

### Community 386 - "Community 386"
Cohesion: 1.0
Nodes (0): 

### Community 387 - "Community 387"
Cohesion: 1.0
Nodes (0): 

### Community 388 - "Community 388"
Cohesion: 1.0
Nodes (0): 

### Community 389 - "Community 389"
Cohesion: 1.0
Nodes (0): 

### Community 390 - "Community 390"
Cohesion: 1.0
Nodes (0): 

### Community 391 - "Community 391"
Cohesion: 1.0
Nodes (0): 

### Community 392 - "Community 392"
Cohesion: 1.0
Nodes (0): 

### Community 393 - "Community 393"
Cohesion: 1.0
Nodes (0): 

### Community 394 - "Community 394"
Cohesion: 1.0
Nodes (0): 

### Community 395 - "Community 395"
Cohesion: 1.0
Nodes (0): 

### Community 396 - "Community 396"
Cohesion: 1.0
Nodes (0): 

### Community 397 - "Community 397"
Cohesion: 1.0
Nodes (0): 

### Community 398 - "Community 398"
Cohesion: 1.0
Nodes (0): 

### Community 399 - "Community 399"
Cohesion: 1.0
Nodes (0): 

### Community 400 - "Community 400"
Cohesion: 1.0
Nodes (0): 

### Community 401 - "Community 401"
Cohesion: 1.0
Nodes (0): 

### Community 402 - "Community 402"
Cohesion: 1.0
Nodes (0): 

### Community 403 - "Community 403"
Cohesion: 1.0
Nodes (0): 

### Community 404 - "Community 404"
Cohesion: 1.0
Nodes (0): 

### Community 405 - "Community 405"
Cohesion: 1.0
Nodes (0): 

### Community 406 - "Community 406"
Cohesion: 1.0
Nodes (0): 

### Community 407 - "Community 407"
Cohesion: 1.0
Nodes (0): 

### Community 408 - "Community 408"
Cohesion: 1.0
Nodes (0): 

### Community 409 - "Community 409"
Cohesion: 1.0
Nodes (0): 

### Community 410 - "Community 410"
Cohesion: 1.0
Nodes (0): 

### Community 411 - "Community 411"
Cohesion: 1.0
Nodes (0): 

### Community 412 - "Community 412"
Cohesion: 1.0
Nodes (0): 

### Community 413 - "Community 413"
Cohesion: 1.0
Nodes (0): 

### Community 414 - "Community 414"
Cohesion: 1.0
Nodes (0): 

### Community 415 - "Community 415"
Cohesion: 1.0
Nodes (0): 

### Community 416 - "Community 416"
Cohesion: 1.0
Nodes (0): 

### Community 417 - "Community 417"
Cohesion: 1.0
Nodes (0): 

### Community 418 - "Community 418"
Cohesion: 1.0
Nodes (0): 

### Community 419 - "Community 419"
Cohesion: 1.0
Nodes (0): 

### Community 420 - "Community 420"
Cohesion: 1.0
Nodes (0): 

### Community 421 - "Community 421"
Cohesion: 1.0
Nodes (0): 

### Community 422 - "Community 422"
Cohesion: 1.0
Nodes (0): 

### Community 423 - "Community 423"
Cohesion: 1.0
Nodes (0): 

### Community 424 - "Community 424"
Cohesion: 1.0
Nodes (0): 

### Community 425 - "Community 425"
Cohesion: 1.0
Nodes (0): 

### Community 426 - "Community 426"
Cohesion: 1.0
Nodes (0): 

### Community 427 - "Community 427"
Cohesion: 1.0
Nodes (0): 

### Community 428 - "Community 428"
Cohesion: 1.0
Nodes (0): 

### Community 429 - "Community 429"
Cohesion: 1.0
Nodes (0): 

### Community 430 - "Community 430"
Cohesion: 1.0
Nodes (0): 

### Community 431 - "Community 431"
Cohesion: 1.0
Nodes (0): 

### Community 432 - "Community 432"
Cohesion: 1.0
Nodes (0): 

### Community 433 - "Community 433"
Cohesion: 1.0
Nodes (0): 

### Community 434 - "Community 434"
Cohesion: 1.0
Nodes (0): 

### Community 435 - "Community 435"
Cohesion: 1.0
Nodes (0): 

### Community 436 - "Community 436"
Cohesion: 1.0
Nodes (0): 

### Community 437 - "Community 437"
Cohesion: 1.0
Nodes (0): 

### Community 438 - "Community 438"
Cohesion: 1.0
Nodes (0): 

### Community 439 - "Community 439"
Cohesion: 1.0
Nodes (0): 

### Community 440 - "Community 440"
Cohesion: 1.0
Nodes (0): 

### Community 441 - "Community 441"
Cohesion: 1.0
Nodes (0): 

### Community 442 - "Community 442"
Cohesion: 1.0
Nodes (0): 

### Community 443 - "Community 443"
Cohesion: 1.0
Nodes (0): 

### Community 444 - "Community 444"
Cohesion: 1.0
Nodes (0): 

### Community 445 - "Community 445"
Cohesion: 1.0
Nodes (0): 

### Community 446 - "Community 446"
Cohesion: 1.0
Nodes (0): 

### Community 447 - "Community 447"
Cohesion: 1.0
Nodes (0): 

### Community 448 - "Community 448"
Cohesion: 1.0
Nodes (0): 

### Community 449 - "Community 449"
Cohesion: 1.0
Nodes (0): 

### Community 450 - "Community 450"
Cohesion: 1.0
Nodes (0): 

### Community 451 - "Community 451"
Cohesion: 1.0
Nodes (0): 

### Community 452 - "Community 452"
Cohesion: 1.0
Nodes (0): 

### Community 453 - "Community 453"
Cohesion: 1.0
Nodes (0): 

### Community 454 - "Community 454"
Cohesion: 1.0
Nodes (0): 

### Community 455 - "Community 455"
Cohesion: 1.0
Nodes (0): 

### Community 456 - "Community 456"
Cohesion: 1.0
Nodes (0): 

### Community 457 - "Community 457"
Cohesion: 1.0
Nodes (0): 

### Community 458 - "Community 458"
Cohesion: 1.0
Nodes (0): 

### Community 459 - "Community 459"
Cohesion: 1.0
Nodes (0): 

### Community 460 - "Community 460"
Cohesion: 1.0
Nodes (0): 

### Community 461 - "Community 461"
Cohesion: 1.0
Nodes (0): 

### Community 462 - "Community 462"
Cohesion: 1.0
Nodes (0): 

### Community 463 - "Community 463"
Cohesion: 1.0
Nodes (0): 

### Community 464 - "Community 464"
Cohesion: 1.0
Nodes (0): 

### Community 465 - "Community 465"
Cohesion: 1.0
Nodes (0): 

### Community 466 - "Community 466"
Cohesion: 1.0
Nodes (0): 

### Community 467 - "Community 467"
Cohesion: 1.0
Nodes (0): 

### Community 468 - "Community 468"
Cohesion: 1.0
Nodes (0): 

### Community 469 - "Community 469"
Cohesion: 1.0
Nodes (0): 

### Community 470 - "Community 470"
Cohesion: 1.0
Nodes (0): 

### Community 471 - "Community 471"
Cohesion: 1.0
Nodes (0): 

### Community 472 - "Community 472"
Cohesion: 1.0
Nodes (0): 

### Community 473 - "Community 473"
Cohesion: 1.0
Nodes (0): 

### Community 474 - "Community 474"
Cohesion: 1.0
Nodes (0): 

### Community 475 - "Community 475"
Cohesion: 1.0
Nodes (0): 

### Community 476 - "Community 476"
Cohesion: 1.0
Nodes (0): 

### Community 477 - "Community 477"
Cohesion: 1.0
Nodes (0): 

### Community 478 - "Community 478"
Cohesion: 1.0
Nodes (0): 

### Community 479 - "Community 479"
Cohesion: 1.0
Nodes (0): 

### Community 480 - "Community 480"
Cohesion: 1.0
Nodes (0): 

### Community 481 - "Community 481"
Cohesion: 1.0
Nodes (0): 

### Community 482 - "Community 482"
Cohesion: 1.0
Nodes (0): 

### Community 483 - "Community 483"
Cohesion: 1.0
Nodes (0): 

### Community 484 - "Community 484"
Cohesion: 1.0
Nodes (0): 

### Community 485 - "Community 485"
Cohesion: 1.0
Nodes (0): 

### Community 486 - "Community 486"
Cohesion: 1.0
Nodes (0): 

### Community 487 - "Community 487"
Cohesion: 1.0
Nodes (0): 

### Community 488 - "Community 488"
Cohesion: 1.0
Nodes (0): 

### Community 489 - "Community 489"
Cohesion: 1.0
Nodes (0): 

### Community 490 - "Community 490"
Cohesion: 1.0
Nodes (0): 

### Community 491 - "Community 491"
Cohesion: 1.0
Nodes (0): 

### Community 492 - "Community 492"
Cohesion: 1.0
Nodes (0): 

### Community 493 - "Community 493"
Cohesion: 1.0
Nodes (0): 

### Community 494 - "Community 494"
Cohesion: 1.0
Nodes (0): 

### Community 495 - "Community 495"
Cohesion: 1.0
Nodes (0): 

### Community 496 - "Community 496"
Cohesion: 1.0
Nodes (0): 

### Community 497 - "Community 497"
Cohesion: 1.0
Nodes (0): 

### Community 498 - "Community 498"
Cohesion: 1.0
Nodes (0): 

### Community 499 - "Community 499"
Cohesion: 1.0
Nodes (0): 

### Community 500 - "Community 500"
Cohesion: 1.0
Nodes (0): 

### Community 501 - "Community 501"
Cohesion: 1.0
Nodes (0): 

### Community 502 - "Community 502"
Cohesion: 1.0
Nodes (0): 

### Community 503 - "Community 503"
Cohesion: 1.0
Nodes (0): 

### Community 504 - "Community 504"
Cohesion: 1.0
Nodes (0): 

### Community 505 - "Community 505"
Cohesion: 1.0
Nodes (0): 

### Community 506 - "Community 506"
Cohesion: 1.0
Nodes (0): 

### Community 507 - "Community 507"
Cohesion: 1.0
Nodes (0): 

### Community 508 - "Community 508"
Cohesion: 1.0
Nodes (0): 

### Community 509 - "Community 509"
Cohesion: 1.0
Nodes (0): 

### Community 510 - "Community 510"
Cohesion: 1.0
Nodes (0): 

### Community 511 - "Community 511"
Cohesion: 1.0
Nodes (0): 

### Community 512 - "Community 512"
Cohesion: 1.0
Nodes (0): 

### Community 513 - "Community 513"
Cohesion: 1.0
Nodes (0): 

### Community 514 - "Community 514"
Cohesion: 1.0
Nodes (0): 

### Community 515 - "Community 515"
Cohesion: 1.0
Nodes (0): 

### Community 516 - "Community 516"
Cohesion: 1.0
Nodes (0): 

### Community 517 - "Community 517"
Cohesion: 1.0
Nodes (0): 

### Community 518 - "Community 518"
Cohesion: 1.0
Nodes (0): 

### Community 519 - "Community 519"
Cohesion: 1.0
Nodes (0): 

### Community 520 - "Community 520"
Cohesion: 1.0
Nodes (0): 

### Community 521 - "Community 521"
Cohesion: 1.0
Nodes (0): 

### Community 522 - "Community 522"
Cohesion: 1.0
Nodes (0): 

### Community 523 - "Community 523"
Cohesion: 1.0
Nodes (0): 

### Community 524 - "Community 524"
Cohesion: 1.0
Nodes (0): 

### Community 525 - "Community 525"
Cohesion: 1.0
Nodes (0): 

### Community 526 - "Community 526"
Cohesion: 1.0
Nodes (0): 

### Community 527 - "Community 527"
Cohesion: 1.0
Nodes (0): 

### Community 528 - "Community 528"
Cohesion: 1.0
Nodes (0): 

### Community 529 - "Community 529"
Cohesion: 1.0
Nodes (0): 

### Community 530 - "Community 530"
Cohesion: 1.0
Nodes (0): 

### Community 531 - "Community 531"
Cohesion: 1.0
Nodes (0): 

### Community 532 - "Community 532"
Cohesion: 1.0
Nodes (0): 

### Community 533 - "Community 533"
Cohesion: 1.0
Nodes (0): 

### Community 534 - "Community 534"
Cohesion: 1.0
Nodes (0): 

### Community 535 - "Community 535"
Cohesion: 1.0
Nodes (0): 

### Community 536 - "Community 536"
Cohesion: 1.0
Nodes (0): 

### Community 537 - "Community 537"
Cohesion: 1.0
Nodes (0): 

### Community 538 - "Community 538"
Cohesion: 1.0
Nodes (0): 

### Community 539 - "Community 539"
Cohesion: 1.0
Nodes (0): 

### Community 540 - "Community 540"
Cohesion: 1.0
Nodes (0): 

### Community 541 - "Community 541"
Cohesion: 1.0
Nodes (0): 

### Community 542 - "Community 542"
Cohesion: 1.0
Nodes (0): 

### Community 543 - "Community 543"
Cohesion: 1.0
Nodes (0): 

### Community 544 - "Community 544"
Cohesion: 1.0
Nodes (0): 

### Community 545 - "Community 545"
Cohesion: 1.0
Nodes (0): 

### Community 546 - "Community 546"
Cohesion: 1.0
Nodes (0): 

### Community 547 - "Community 547"
Cohesion: 1.0
Nodes (0): 

### Community 548 - "Community 548"
Cohesion: 1.0
Nodes (0): 

### Community 549 - "Community 549"
Cohesion: 1.0
Nodes (0): 

### Community 550 - "Community 550"
Cohesion: 1.0
Nodes (0): 

### Community 551 - "Community 551"
Cohesion: 1.0
Nodes (0): 

### Community 552 - "Community 552"
Cohesion: 1.0
Nodes (0): 

### Community 553 - "Community 553"
Cohesion: 1.0
Nodes (0): 

### Community 554 - "Community 554"
Cohesion: 1.0
Nodes (0): 

### Community 555 - "Community 555"
Cohesion: 1.0
Nodes (0): 

### Community 556 - "Community 556"
Cohesion: 1.0
Nodes (0): 

### Community 557 - "Community 557"
Cohesion: 1.0
Nodes (0): 

### Community 558 - "Community 558"
Cohesion: 1.0
Nodes (0): 

### Community 559 - "Community 559"
Cohesion: 1.0
Nodes (0): 

### Community 560 - "Community 560"
Cohesion: 1.0
Nodes (0): 

### Community 561 - "Community 561"
Cohesion: 1.0
Nodes (0): 

### Community 562 - "Community 562"
Cohesion: 1.0
Nodes (0): 

### Community 563 - "Community 563"
Cohesion: 1.0
Nodes (0): 

### Community 564 - "Community 564"
Cohesion: 1.0
Nodes (0): 

### Community 565 - "Community 565"
Cohesion: 1.0
Nodes (0): 

### Community 566 - "Community 566"
Cohesion: 1.0
Nodes (0): 

### Community 567 - "Community 567"
Cohesion: 1.0
Nodes (0): 

### Community 568 - "Community 568"
Cohesion: 1.0
Nodes (0): 

### Community 569 - "Community 569"
Cohesion: 1.0
Nodes (0): 

### Community 570 - "Community 570"
Cohesion: 1.0
Nodes (0): 

### Community 571 - "Community 571"
Cohesion: 1.0
Nodes (0): 

### Community 572 - "Community 572"
Cohesion: 1.0
Nodes (0): 

### Community 573 - "Community 573"
Cohesion: 1.0
Nodes (0): 

### Community 574 - "Community 574"
Cohesion: 1.0
Nodes (0): 

### Community 575 - "Community 575"
Cohesion: 1.0
Nodes (0): 

### Community 576 - "Community 576"
Cohesion: 1.0
Nodes (0): 

### Community 577 - "Community 577"
Cohesion: 1.0
Nodes (0): 

### Community 578 - "Community 578"
Cohesion: 1.0
Nodes (0): 

### Community 579 - "Community 579"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **166 isolated node(s):** `BLE gateway WebSocket connection manager bridging main.py and ha_client.py.  T`, `FastAPI application orchestrator for the ProjectNemo aquarium monitoring system.`, `Add new columns to existing tables. SQLite-safe: errors mean column exists.`, `Pydantic schemas for API request/response validation.`, `Try full latin, then genus+species (skipping cf./sp./var.), then genus only.` (+161 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 195`** (2 nodes): `__init__.py`, `Fluval Shaker RGBW BLE custom component for Home Assistant.  Extends mrzottel/`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 196`** (2 nodes): `babel-parser.d.ts`, `Position`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 197`** (2 nodes): `assertNode.js`, `assertNode()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 198`** (2 nodes): `createFlowUnionType.js`, `createFlowUnionType()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 199`** (2 nodes): `createTypeAnnotationBasedOnTypeof.js`, `createTypeAnnotationBasedOnTypeof()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 200`** (2 nodes): `uppercase.js`, `alias()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 201`** (2 nodes): `productions.js`, `buildUndefinedNode()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 202`** (2 nodes): `buildChildren.js`, `buildChildren()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 203`** (2 nodes): `createTSUnionType.js`, `createTSUnionType()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 204`** (2 nodes): `validateNode.js`, `validateNode()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 205`** (2 nodes): `clone.js`, `clone()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 206`** (2 nodes): `cloneDeep.js`, `cloneDeep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 207`** (2 nodes): `cloneDeepWithoutLoc.js`, `cloneDeepWithoutLoc()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 208`** (2 nodes): `cloneWithoutLoc.js`, `cloneWithoutLoc()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 209`** (2 nodes): `addComment.js`, `addComment()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 210`** (2 nodes): `addComments.js`, `addComments()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 211`** (2 nodes): `inheritInnerComments.js`, `inheritInnerComments()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 212`** (2 nodes): `inheritLeadingComments.js`, `inheritLeadingComments()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 213`** (2 nodes): `inheritsComments.js`, `inheritsComments()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 214`** (2 nodes): `inheritTrailingComments.js`, `inheritTrailingComments()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 215`** (2 nodes): `removeComments.js`, `removeComments()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 216`** (2 nodes): `ensureBlock.js`, `ensureBlock()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 217`** (2 nodes): `gatherSequenceExpressions.js`, `gatherSequenceExpressions()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 218`** (2 nodes): `toBindingIdentifierName.js`, `toBindingIdentifierName()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 219`** (2 nodes): `toBlock.js`, `toBlock()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 220`** (2 nodes): `toComputedKey.js`, `toComputedKey()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 221`** (2 nodes): `toExpression.js`, `toExpression()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 222`** (2 nodes): `toIdentifier.js`, `toIdentifier()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 223`** (2 nodes): `toKeyAlias.js`, `toKeyAlias()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 224`** (2 nodes): `toSequenceExpression.js`, `toSequenceExpression()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 225`** (2 nodes): `toStatement.js`, `toStatement()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 226`** (2 nodes): `flow.js`, `defineInterfaceishType()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 227`** (2 nodes): `appendToMemberExpression.js`, `appendToMemberExpression()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 228`** (2 nodes): `inherits.js`, `inherits()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 229`** (2 nodes): `prependToMemberExpression.js`, `prependToMemberExpression()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 230`** (2 nodes): `removeProperties.js`, `removeProperties()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 231`** (2 nodes): `removePropertiesDeep.js`, `removePropertiesDeep()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 232`** (2 nodes): `getAssignmentIdentifiers.js`, `getAssignmentIdentifiers()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 233`** (2 nodes): `getBindingIdentifiers.js`, `getBindingIdentifiers()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 234`** (2 nodes): `getOuterBindingIdentifiers.js`, `getOuterBindingIdentifiers()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 235`** (2 nodes): `traverseFast.js`, `traverseFast()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 236`** (2 nodes): `inherit.js`, `inherit()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 237`** (2 nodes): `cleanJSXElementLiteralChild.js`, `cleanJSXElementLiteralChild()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 238`** (2 nodes): `shallowEqual.js`, `shallowEqual()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 239`** (2 nodes): `buildMatchMemberExpression.js`, `buildMatchMemberExpression()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 240`** (2 nodes): `is.js`, `is()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 241`** (2 nodes): `isBinding.js`, `isBinding()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 242`** (2 nodes): `isBlockScoped.js`, `isBlockScoped()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 243`** (2 nodes): `isImmutable.js`, `isImmutable()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 244`** (2 nodes): `isLet.js`, `isLet()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 245`** (2 nodes): `isNode.js`, `isNode()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 246`** (2 nodes): `isNodesEquivalent.js`, `isNodesEquivalent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 247`** (2 nodes): `isPlaceholderType.js`, `isPlaceholderType()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 248`** (2 nodes): `isReferenced.js`, `isReferenced()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 249`** (2 nodes): `isScope.js`, `isScope()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 250`** (2 nodes): `isSpecifierDefault.js`, `isSpecifierDefault()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 251`** (2 nodes): `isType.js`, `isType()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 252`** (2 nodes): `isValidES3Identifier.js`, `isValidES3Identifier()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 253`** (2 nodes): `isValidIdentifier.js`, `isValidIdentifier()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 254`** (2 nodes): `isVar.js`, `isVar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 255`** (2 nodes): `isCompatTag.js`, `isCompatTag()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 256`** (2 nodes): `color.d.ts`, `Color`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 257`** (2 nodes): `proxy.d.ts`, `ApiProxy`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 258`** (2 nodes): `runtime-dom.d.ts`, `VueElement`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 259`** (2 nodes): `defer.js`, `defer()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 260`** (2 nodes): `readable_parallel.js`, `ReadableParallel()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 261`** (2 nodes): `readable_serial.js`, `ReadableSerial()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 262`** (2 nodes): `readable_serial_ordered.js`, `ReadableSerialOrdered()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 263`** (2 nodes): `state.js`, `state()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 264`** (2 nodes): `terminator.js`, `terminator()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 265`** (2 nodes): `parallel.js`, `parallel()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 266`** (2 nodes): `serial.js`, `serial()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 267`** (2 nodes): `isCancel.js`, `isCancel()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 268`** (2 nodes): `setFormDataHeaders.js`, `setFormDataHeaders()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 269`** (2 nodes): `settle.js`, `settle()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 270`** (2 nodes): `transformData.js`, `transformData()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 271`** (2 nodes): `bind.js`, `bind()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 272`** (2 nodes): `callbackify.js`, `callbackify()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 273`** (2 nodes): `combineURLs.js`, `combineURLs()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 274`** (2 nodes): `composeSignals.js`, `composeSignals()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 275`** (2 nodes): `deprecatedMethod.js`, `deprecatedMethod()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 276`** (2 nodes): `fromDataURI.js`, `fromDataURI()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 277`** (2 nodes): `isAbsoluteURL.js`, `isAbsoluteURL()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 278`** (2 nodes): `isAxiosError.js`, `isAxiosError()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 279`** (2 nodes): `parseProtocol.js`, `parseProtocol()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 280`** (2 nodes): `speedometer.js`, `speedometer()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 281`** (2 nodes): `spread.js`, `spread()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 282`** (2 nodes): `throttle.js`, `throttle()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 283`** (2 nodes): `toURLEncodedForm.js`, `toURLEncodedForm()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 284`** (2 nodes): `trackStream.js`, `trackStream()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 285`** (2 nodes): `actualApply.js`, `applyBind.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 286`** (2 nodes): `controller.bar.d.ts`, `BarController`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 287`** (2 nodes): `controller.bubble.d.ts`, `BubbleController`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 288`** (2 nodes): `controller.doughnut.d.ts`, `DoughnutController`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 289`** (2 nodes): `controller.line.d.ts`, `LineController`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 290`** (2 nodes): `controller.pie.d.ts`, `PieController`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 291`** (2 nodes): `controller.polarArea.d.ts`, `PolarAreaController`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 292`** (2 nodes): `controller.radar.d.ts`, `RadarController`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 293`** (2 nodes): `controller.scatter.d.ts`, `ScatterController`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 294`** (2 nodes): `core.animation.d.ts`, `Animation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 295`** (2 nodes): `core.animations.d.ts`, `Animations`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 296`** (2 nodes): `core.animator.d.ts`, `Animator`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 297`** (2 nodes): `core.config.d.ts`, `Config`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 298`** (2 nodes): `core.controller.d.ts`, `Chart`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 299`** (2 nodes): `core.datasetController.d.ts`, `DatasetController`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 300`** (2 nodes): `core.defaults.d.ts`, `Defaults`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 301`** (2 nodes): `core.element.d.ts`, `Element`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 302`** (2 nodes): `core.plugins.d.ts`, `PluginService`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 303`** (2 nodes): `core.registry.d.ts`, `Registry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 304`** (2 nodes): `core.typedRegistry.d.ts`, `TypedRegistry`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 305`** (2 nodes): `element.arc.d.ts`, `ArcElement`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 306`** (2 nodes): `element.bar.d.ts`, `BarElement`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 307`** (2 nodes): `element.point.d.ts`, `PointElement`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 308`** (2 nodes): `platform.base.d.ts`, `BasePlatform`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 309`** (2 nodes): `platform.basic.d.ts`, `BasicPlatform`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 310`** (2 nodes): `platform.dom.d.ts`, `DomPlatform`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 311`** (2 nodes): `simpleArc.d.ts`, `simpleArc`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 312`** (2 nodes): `plugin.legend.d.ts`, `constructor()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 313`** (2 nodes): `plugin.title.d.ts`, `constructor()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 314`** (2 nodes): `plugin.tooltip.d.ts`, `Tooltip`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 315`** (2 nodes): `scale.category.d.ts`, `CategoryScale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 316`** (2 nodes): `scale.linear.d.ts`, `LinearScale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 317`** (2 nodes): `scale.linearbase.d.ts`, `LinearScaleBase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 318`** (2 nodes): `scale.logarithmic.d.ts`, `LogarithmicScale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 319`** (2 nodes): `scale.radialLinear.d.ts`, `RadialLinearScale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 320`** (2 nodes): `scale.time.d.ts`, `TimeScale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 321`** (2 nodes): `scale.timeseries.d.ts`, `TimeSeriesScale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 322`** (2 nodes): `combined_stream.js`, `CombinedStream()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 323`** (2 nodes): `common.js`, `setup()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 324`** (2 nodes): `delayed_stream.js`, `DelayedStream()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 325`** (2 nodes): `decode.d.ts`, `EntityDecoder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 326`** (2 nodes): `decode-shared.ts`, `decodeBase64()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 327`** (2 nodes): `encode-shared.ts`, `parseEncodeTrie()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 328`** (2 nodes): `async.d.ts`, `AsyncWalker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 329`** (2 nodes): `sync.d.ts`, `SyncWalker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 330`** (2 nodes): `walker.d.ts`, `WalkerBase`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 331`** (2 nodes): `agent.d.ts`, `HttpsProxyAgent`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 332`** (2 nodes): `parse-proxy-response.js`, `parseProxyResponse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 333`** (2 nodes): `nanoid.js`, `nanoid()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 334`** (2 nodes): `at-rule.d.ts`, `AtRule_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 335`** (2 nodes): `comment.d.ts`, `Comment_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 336`** (2 nodes): `container.d.ts`, `Container`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 337`** (2 nodes): `css-syntax-error.d.ts`, `CssSyntaxError_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 338`** (2 nodes): `declaration.d.ts`, `Declaration_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 339`** (2 nodes): `document.d.ts`, `Document_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 340`** (2 nodes): `input.d.ts`, `Input_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 341`** (2 nodes): `lazy-result.d.ts`, `LazyResult_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 342`** (2 nodes): `no-work-result.d.ts`, `NoWorkResult_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 343`** (2 nodes): `node.d.ts`, `Node`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 344`** (2 nodes): `parse.js`, `parse()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 345`** (2 nodes): `previous-map.d.ts`, `PreviousMap_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 346`** (2 nodes): `processor.d.ts`, `Processor_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 347`** (2 nodes): `result.d.ts`, `Result_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 348`** (2 nodes): `root.d.ts`, `Root_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 349`** (2 nodes): `rule.d.ts`, `Rule_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 350`** (2 nodes): `stringifier.d.ts`, `Stringifier_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 351`** (2 nodes): `stringify.js`, `stringify()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 352`** (2 nodes): `warning.d.ts`, `Warning_`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 353`** (2 nodes): `array-set.js`, `ArraySet()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 354`** (2 nodes): `binary-search.js`, `recursiveSearch()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 355`** (2 nodes): `source-map-generator.js`, `SourceMapGenerator()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 356`** (2 nodes): `index.iife.js`, `createApp()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 357`** (1 nodes): `babel-parser.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 358`** (1 nodes): `deprecated-aliases.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 359`** (1 nodes): `experimental.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 360`** (1 nodes): `jsx.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 361`** (1 nodes): `misc.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 362`** (1 nodes): `placeholders.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 363`** (1 nodes): `index-legacy.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 364`** (1 nodes): `isReactComponent.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 365`** (1 nodes): `core-base.cjs.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 366`** (1 nodes): `core-base.cjs.prod.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 367`** (1 nodes): `core-base.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 368`** (1 nodes): `core-base.esm-bundler.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 369`** (1 nodes): `message-compiler.cjs.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 370`** (1 nodes): `message-compiler.cjs.prod.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 371`** (1 nodes): `message-compiler.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 372`** (1 nodes): `message-compiler.esm-bundler.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 373`** (1 nodes): `shared.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 374`** (1 nodes): `flow.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 375`** (1 nodes): `compiler-dom.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 376`** (1 nodes): `compiler-ssr.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 377`** (1 nodes): `api.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 378`** (1 nodes): `app.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 379`** (1 nodes): `component.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 380`** (1 nodes): `context.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 381`** (1 nodes): `hooks.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 382`** (1 nodes): `const.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 383`** (1 nodes): `plugin.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 384`** (1 nodes): `api.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 385`** (1 nodes): `app.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 386`** (1 nodes): `component.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 387`** (1 nodes): `context.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 388`** (1 nodes): `hooks.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 389`** (1 nodes): `util.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 390`** (1 nodes): `const.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 391`** (1 nodes): `env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 392`** (1 nodes): `plugin.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 393`** (1 nodes): `time.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 394`** (1 nodes): `runtime-core.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 395`** (1 nodes): `server-renderer.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 396`** (1 nodes): `bench.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 397`** (1 nodes): `transitional.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 398`** (1 nodes): `data.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 399`** (1 nodes): `HttpStatusCode.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 400`** (1 nodes): `isURLSameOrigin.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 401`** (1 nodes): `null.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 402`** (1 nodes): `parseHeaders.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 403`** (1 nodes): `readBlob.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 404`** (1 nodes): `Blob.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 405`** (1 nodes): `URLSearchParams.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 406`** (1 nodes): `actualApply.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 407`** (1 nodes): `applyBind.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 408`** (1 nodes): `functionApply.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 409`** (1 nodes): `functionApply.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 410`** (1 nodes): `functionCall.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 411`** (1 nodes): `functionCall.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 412`** (1 nodes): `reflectApply.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 413`** (1 nodes): `reflectApply.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 414`** (1 nodes): `auto.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 415`** (1 nodes): `auto.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 416`** (1 nodes): `core.adapters.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 417`** (1 nodes): `core.animations.defaults.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 418`** (1 nodes): `core.interaction.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 419`** (1 nodes): `core.layouts.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 420`** (1 nodes): `core.layouts.defaults.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 421`** (1 nodes): `core.scale.autoskip.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 422`** (1 nodes): `core.scale.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 423`** (1 nodes): `core.scale.defaults.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 424`** (1 nodes): `core.ticks.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 425`** (1 nodes): `element.line.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 426`** (1 nodes): `helpers.canvas.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 427`** (1 nodes): `helpers.collection.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 428`** (1 nodes): `helpers.color.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 429`** (1 nodes): `helpers.config.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 430`** (1 nodes): `helpers.config.types.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 431`** (1 nodes): `helpers.core.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 432`** (1 nodes): `helpers.curve.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 433`** (1 nodes): `helpers.dataset.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 434`** (1 nodes): `helpers.dom.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 435`** (1 nodes): `helpers.easing.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 436`** (1 nodes): `helpers.extras.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 437`** (1 nodes): `helpers.interpolation.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 438`** (1 nodes): `helpers.intl.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 439`** (1 nodes): `helpers.math.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 440`** (1 nodes): `helpers.options.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 441`** (1 nodes): `helpers.rtl.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 442`** (1 nodes): `helpers.segment.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 443`** (1 nodes): `helpers.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 444`** (1 nodes): `index.umd.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 445`** (1 nodes): `plugin.colors.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 446`** (1 nodes): `plugin.decimation.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 447`** (1 nodes): `filler.drawing.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 448`** (1 nodes): `filler.helper.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 449`** (1 nodes): `filler.options.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 450`** (1 nodes): `filler.segment.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 451`** (1 nodes): `filler.target.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 452`** (1 nodes): `filler.target.stack.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 453`** (1 nodes): `plugin.subtitle.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 454`** (1 nodes): `basic.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 455`** (1 nodes): `geometric.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 456`** (1 nodes): `layout.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 457`** (1 nodes): `utils.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 458`** (1 nodes): `types.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 459`** (1 nodes): `helpers.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 460`** (1 nodes): `get.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 461`** (1 nodes): `get.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 462`** (1 nodes): `set.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 463`** (1 nodes): `set.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 464`** (1 nodes): `decode-codepoint.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 465`** (1 nodes): `encode.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 466`** (1 nodes): `escape.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 467`** (1 nodes): `decode-data-html.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 468`** (1 nodes): `decode-data-html.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 469`** (1 nodes): `decode-data-xml.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 470`** (1 nodes): `decode-data-xml.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 471`** (1 nodes): `encode-html.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 472`** (1 nodes): `encode-html.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 473`** (1 nodes): `bin-trie-flags.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 474`** (1 nodes): `bin-trie-flags.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 475`** (1 nodes): `decode-shared.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 476`** (1 nodes): `encode-shared.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 477`** (1 nodes): `eval.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 478`** (1 nodes): `eval.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 479`** (1 nodes): `range.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 480`** (1 nodes): `range.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 481`** (1 nodes): `ref.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 482`** (1 nodes): `ref.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 483`** (1 nodes): `syntax.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 484`** (1 nodes): `syntax.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 485`** (1 nodes): `type.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 486`** (1 nodes): `type.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 487`** (1 nodes): `uri.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 488`** (1 nodes): `uri.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 489`** (1 nodes): `isObject.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 490`** (1 nodes): `isObject.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 491`** (1 nodes): `RequireObjectCoercible.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 492`** (1 nodes): `RequireObjectCoercible.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 493`** (1 nodes): `ToObject.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 494`** (1 nodes): `ToObject.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 495`** (1 nodes): `main.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 496`** (1 nodes): `populate.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 497`** (1 nodes): `implementation.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 498`** (1 nodes): `GetIntrinsic.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 499`** (1 nodes): `Object.getPrototypeOf.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 500`** (1 nodes): `Object.getPrototypeOf.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 501`** (1 nodes): `Reflect.getPrototypeOf.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 502`** (1 nodes): `Reflect.getPrototypeOf.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 503`** (1 nodes): `gOPD.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 504`** (1 nodes): `gOPD.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 505`** (1 nodes): `shams.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 506`** (1 nodes): `shams.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 507`** (1 nodes): `core-js.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 508`** (1 nodes): `get-own-property-symbols.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 509`** (1 nodes): `tests.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 510`** (1 nodes): `abs.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 511`** (1 nodes): `abs.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 512`** (1 nodes): `maxArrayLength.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 513`** (1 nodes): `maxArrayLength.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 514`** (1 nodes): `maxSafeInteger.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 515`** (1 nodes): `maxSafeInteger.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 516`** (1 nodes): `maxValue.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 517`** (1 nodes): `maxValue.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 518`** (1 nodes): `floor.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 519`** (1 nodes): `floor.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 520`** (1 nodes): `isFinite.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 521`** (1 nodes): `isFinite.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 522`** (1 nodes): `isInteger.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 523`** (1 nodes): `isInteger.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 524`** (1 nodes): `isNaN.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 525`** (1 nodes): `isNaN.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 526`** (1 nodes): `isNegativeZero.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 527`** (1 nodes): `isNegativeZero.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 528`** (1 nodes): `max.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 529`** (1 nodes): `max.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 530`** (1 nodes): `min.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 531`** (1 nodes): `min.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 532`** (1 nodes): `mod.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 533`** (1 nodes): `mod.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 534`** (1 nodes): `pow.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 535`** (1 nodes): `pow.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 536`** (1 nodes): `round.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 537`** (1 nodes): `round.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 538`** (1 nodes): `sign.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 539`** (1 nodes): `sign.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 540`** (1 nodes): `picocolors.browser.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 541`** (1 nodes): `picocolors.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 542`** (1 nodes): `pinia.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 543`** (1 nodes): `fromJSON.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 544`** (1 nodes): `list.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 545`** (1 nodes): `list.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 546`** (1 nodes): `parse.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 547`** (1 nodes): `postcss.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 548`** (1 nodes): `stringify.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 549`** (1 nodes): `symbols.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 550`** (1 nodes): `warn-once.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 551`** (1 nodes): `rollup.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 552`** (1 nodes): `source-map-consumer.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 553`** (1 nodes): `source-map-generator.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 554`** (1 nodes): `source-node.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 555`** (1 nodes): `source-map.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 556`** (1 nodes): `client.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 557`** (1 nodes): `constants.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 558`** (1 nodes): `customEvent.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 559`** (1 nodes): `hmrPayload.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 560`** (1 nodes): `hot.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 561`** (1 nodes): `import-meta.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 562`** (1 nodes): `importGlob.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 563`** (1 nodes): `importMeta.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 564`** (1 nodes): `metadata.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 565`** (1 nodes): `register-ts.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 566`** (1 nodes): `vue.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 567`** (1 nodes): `jsx.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 568`** (1 nodes): `chart.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 569`** (1 nodes): `props.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 570`** (1 nodes): `typedCharts.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 571`** (1 nodes): `vue-demi-fix.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 572`** (1 nodes): `vue-demi-switch.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 573`** (1 nodes): `postinstall.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 574`** (1 nodes): `switch-cli.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 575`** (1 nodes): `vue-i18n.cjs.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 576`** (1 nodes): `vue-i18n.cjs.prod.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 577`** (1 nodes): `vue-i18n.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 578`** (1 nodes): `vue-i18n.esm-bundler.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 579`** (1 nodes): `vue-i18n.runtime.esm-bundler.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 310 inferred relationships involving `assert()` (e.g. with `tsParseType()` and `parseMaybeAssign()`) actually correct?**
  _`assert()` has 310 INFERRED edges - model-reasoned connections that need verification._
- **Are the 158 inferred relationships involving `push()` (e.g. with `scan$2()` and `parse$g()`) actually correct?**
  _`push()` has 158 INFERRED edges - model-reasoned connections that need verification._
- **What connects `BLE gateway WebSocket connection manager bridging main.py and ha_client.py.  T`, `FastAPI application orchestrator for the ProjectNemo aquarium monitoring system.`, `Add new columns to existing tables. SQLite-safe: errors mean column exists.` to the rest of the system?**
  _166 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.0 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.0 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.0 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.0 - nodes in this community are weakly interconnected._