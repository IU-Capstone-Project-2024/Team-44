from rest_framework import serializers


class SummarySerializer(serializers.Serializer):
    text = serializers.CharField()


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField())
    correct_answers = serializers.ListField(child=serializers.CharField())


class QuizSerializer(serializers.Serializer):
    questions = QuestionSerializer(many=True)


class TextSerializer(serializers.Serializer):
    text = serializers.CharField()
