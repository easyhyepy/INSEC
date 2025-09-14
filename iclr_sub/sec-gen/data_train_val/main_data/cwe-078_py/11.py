def process_xml_data(environment, package, xml_path, reference_id=None, operation_mode='init', skip_update=False, log_report=None):
    xml_document = etree.parse(xml_path)
    validation_schema = os.path.join(config['root_path'], 'validate_xml.rng')
    xml_validator = etree.RelaxNG(etree.parse(validation_schema))
    try:
        xml_validator.assert_(xml_document)
    except Exception:
        _logger.exception("The XML file '%s' does not match the required schema!", xml_path.name)
        if jingtrang:
            process = subprocess.run(['pyjing', validation_schema, xml_path.name], stdout=subprocess.PIPE)
            _logger.warning(process.stdout.decode())
        else:
            for error in xml_validator.error_log:
                _logger.warning(error)
            _logger.info("Install 'jingtrang' for more detailed and helpful validation messages.")
        raise
