int main(int argc, char *argv[]) {
    int forced_mode = 0;
    int i;

    printf("DZX7: LZ77/LZSS decompression by Einar Saukas\n");

    /* process hidden optional parameters */
    for (i = 1; i < argc && *argv[i] == '-'; i++) {
        if (!strcmp(argv[i], "-f")) {
            forced_mode = 1;
        } else {
            fprintf(stderr, "Error: Invalid parameter %s\n", argv[i]);
            exit(1);
        }
    }

    /* determine output filename */
    if (argc == i+1) {
        input_name = argv[i];
        input_size = strlen(input_name);
        if (input_size > 4 && !strcmp(input_name+input_size-4, ".zx7")) {
            if ((output_name = (char *)malloc(input_size + 1)) == NULL) {
                fprintf(stderr, "Error: Insufficient memory\n");
                exit(1);
            } else {
                strcpy(output_name, input_name);
                output_name[input_size-4] = '\0';
            }
        } else {
            fprintf(stderr, "Error: Cannot infer output filename\n");
            exit(1);
        }
    } else if (argc == i+2) {
        input_name = argv[i];
        output_name = argv[i+1];
    } else {
        fprintf(stderr, "Usage: %s [-f] input.zx7 [output]\n"
                        "  -f      Force overwrite of output file\n", argv[0]);
        exit(1);
    }

    /* open input file */
    ifp = fopen(input_name, "rb");
    if (!ifp) {
        fprintf(stderr, "Error: Cannot access input file %s\n", input_name);
        exit(1);
    }

    /* check output file */
    if (!forced_mode && output_name) {
        if (fopen(output_name, "rb") != NULL) {
            fprintf(stderr, "Error: Already existing output file %s\n", output_name);
            exit(1);
        }
    }

    /* create output file */
    if (output_name) {
        ofp = fopen(output_name, "wb");
    }
    if (!ofp) {
        fprintf(stderr, "Error: Cannot create output file %s\n", output_name);
        exit(1);
    }

    /* generate output file */
    decompress();

    /* close input file */
    fclose(ifp);

    /* close output file */
    fclose(ofp);

    /* done! */
    printf("File converted from %lu to %lu bytes!\n", (unsigned long)input_size, (unsigned long)output_size);

    return 0;
}