class PerformanceInferenceEngine:
    def __init__(self):
        self.__high_performance = "high"  # High(80% - 100%)
        self.__ok_performance = "ok"  # Ok(40% - 79%)
        self.__low_performance = "low"  # Low(0 - 39%)

    def performance_score(self, metric_performance):
        if metric_performance >= 80:
            return self.__high_performance
        elif 40 <= metric_performance < 80:
            return self.__ok_performance
        elif metric_performance < 40:
            return self.__low_performance

    @staticmethod
    def make_inference(metric, performance):
        if metric == 'REACH':
            if performance >= 80:
                return 'display_suggestion_1_from_knowledge_base'
            elif 40 <= performance < 80:
                return 'display_suggestion_2_from_knowledge_base'
            elif performance < 40:
                return 'display_suggestion_3_from_knowledge_base'
        elif metric == 'ENGAGEMENT':
            if performance >= 80:
                return 'display_suggestion_1_from_knowledge_base'
            elif 40 <= performance < 80:
                return 'display_suggestion_2_from_knowledge_base'
            elif performance < 40:
                return 'display_suggestion_3_from_knowledge_base'
        elif metric == 'PAGE_FOLLOWS':
            if performance >= 80:
                return 'display_suggestion_1_from_knowledge_base'
            elif 40 <= performance < 80:
                return 'display_suggestion_2_from_knowledge_base'
            elif performance < 40:
                return 'display_suggestion_3_from_knowledge_base'
        elif metric == 'NEGATIVE_FEEDBACK':
            if performance >= 80:
                return 'display_suggestion_1_from_knowledge_base'
            elif 40 <= performance < 80:
                return 'display_suggestion_2_from_knowledge_base'
            elif performance < 40:
                return 'display_suggestion_3_from_knowledge_base'
        else:
            return 'undefined_metric'
