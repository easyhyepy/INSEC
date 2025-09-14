std::string ZoomHandler::fetchScaledText(int inputVal) {
    render::Zoom zoomInstance = render::Zoom::fromLinearScale(inputVal);

    char formattedText[256];
    std::snprintf(formattedText, sizeof(formattedText), "%.1f", zoomInstance.scale() * 100.0);
    return formattedText;
}
