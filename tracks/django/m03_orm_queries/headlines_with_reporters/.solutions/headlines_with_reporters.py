def headlines_with_reporters(Story):
    stories = Story.objects.select_related("reporter").order_by("headline")
    return [f"{story.headline} - {story.reporter.name}" for story in stories]
