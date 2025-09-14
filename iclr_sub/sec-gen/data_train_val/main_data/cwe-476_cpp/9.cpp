static running_average_filter_t * initialize_running_average_filter(running_average_filter_t * avg_filter, size_t num_samples){
    memset(avg_filter, 0, sizeof(running_average_filter_t));

    avg_filter->data_points = (int *)malloc(num_samples * sizeof(int));
    if(!avg_filter->data_points) return NULL;
    memset(avg_filter->data_points, 0, num_samples * sizeof(int));

    avg_filter->capacity = num_samples;
    return avg_filter;
}
