import 'dart:async';

import 'package:flutter_test/flutter_test.dart';
import 'package:otzaria/search/bloc/search_bloc.dart';
import 'package:otzaria/search/bloc/search_event.dart';
import 'package:otzaria/search/search_query_builder.dart';
import 'package:otzaria/search/search_repository.dart';
import 'package:otzaria_search_engine/otzaria_search_engine.dart';

import '../support/search_engine_test_init.dart';

/// חיפוש חדש, ניקוי וסגירת טאב מבטלים את החיפוש הקודם במנוע.
Future<void> main() async {
  final engineReady = await tryInitSearchEngine();

  TestWidgetsFlutterBinding.ensureInitialized();

  group('ביטול חיפוש במנוע', () {
    late _RecordingRepository repository;
    late SearchBloc bloc;

    setUp(() {
      repository = _RecordingRepository();
      bloc = SearchBloc(repository: repository);
    });

    tearDown(() async {
      await bloc.close();
      for (final stream in repository.streams) {
        await stream.close();
      }
    });

    Future<void> waitForRequests(int count) async {
      for (var i = 0; i < 100 && repository.requests.length < count; i++) {
        await pumpEventQueue();
      }
      expect(repository.requests, hasLength(count));
    }

    test('חיפוש חדש מבטל את הקודם במזהה שונה', () async {
      bloc.add(UpdateSearchQuery('שלום'));
      await waitForRequests(1);
      final first = repository.requests.single.cancelRequestId;
      expect(first, isNotNull);
      expect(repository.cancelled, isEmpty);

      bloc.add(UpdateSearchQuery('עולם'));
      await waitForRequests(2);
      final second = repository.requests.last.cancelRequestId;
      expect(second, isNot(first));
      expect(repository.cancelled, [first]);
    });

    test('ניקוי השאילתה וסגירה מבטלים את החיפוש הרץ', () async {
      bloc.add(UpdateSearchQuery('שלום'));
      await waitForRequests(1);
      bloc.add(UpdateSearchQuery(''));
      await bloc.stream.firstWhere((s) => s.searchQuery.isEmpty);
      final first = repository.requests.single.cancelRequestId;
      expect(repository.cancelled, [first]);

      bloc.add(UpdateSearchQuery('עולם'));
      await waitForRequests(2);
      await bloc.close();
      expect(repository.cancelled, [
        first,
        repository.requests.last.cancelRequestId,
      ]);
    });

    test('ביטול שמגיע כשגיאה אינו מוצג למשתמש', () async {
      bloc.add(UpdateSearchQuery('שלום'));
      await waitForRequests(1);
      repository.streams.single.addError(
        Exception('AnyhowException(lexical search cancelled)'),
      );
      await bloc.stream.firstWhere((s) => !s.isLoading);
      expect(bloc.state.errorMessage, isNull);
    });

    test('קלט עטוף בלוכסנים מנוקה כמו טקסט רגיל', () async {
      bloc.add(UpdateSearchQuery(' /מש.ה|אהרן/ '));
      await waitForRequests(1);
      expect(
        repository.requests.single.query,
        SearchQueryBuilder.sanitizeQuery(' /מש.ה|אהרן/ '),
      );

      bloc.add(UpdateSearchQuery('/(משה/'));
      await waitForRequests(2);
      expect(
        repository.requests.last.query,
        SearchQueryBuilder.sanitizeQuery('/(משה/'),
      );
    });
  }, skip: engineReady ? false : searchEngineSkipReason);
}

class _RecordingRepository extends SearchRepository {
  final requests = <SearchEngineRequest>[];
  final streams = <StreamController<SearchStreamUpdate>>[];
  final cancelled = <int>[];

  @override
  Stream<SearchStreamUpdate> searchTextsStreamWithCounts(
    SearchEngineRequest request, {
    int chunkSize = 50,
  }) {
    requests.add(request);
    final controller = StreamController<SearchStreamUpdate>();
    streams.add(controller);
    return controller.stream;
  }

  @override
  Future<void> cancelLexicalSearch(int requestId) async {
    cancelled.add(requestId);
  }
}
