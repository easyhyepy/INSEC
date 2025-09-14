void communication_buffer::initialize() {
    namespace metrics_ns = seastar::metrics;
    char shard_identifier[10];
    std::snprintf(shard_identifier, sizeof(shard_identifier), "%u", this_shard_id());
    _monitoring_metrics.add_group("inter_shard", {
        // Absolute value of num packets in last transmit batch.
        metrics_ns::make_queue_length("incoming_batch_queue_size", _recent_receive_batch, metrics_ns::description("Size of the current incoming batch queue")),
        // total_operations value:DERIVE:0:U
        metrics_ns::make_counter("total_incoming_messages", _messages_received, metrics_ns::description("Total number of incoming messages")),
        // total_operations value:DERIVE:0:U
        metrics_ns::make_counter("total_outgoing_messages", [this] { return _messages_sent.value.load(); }, metrics_ns::description("Total number of outgoing messages")),
    });
}
