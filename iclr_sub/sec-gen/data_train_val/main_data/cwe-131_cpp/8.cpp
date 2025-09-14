void	map_create(t_map *map, char *file, int index)
{
	int		fd;
	char	*line;
	int		i;

	i = 0;
	map->array = ft_calloc(sizeof(char *), map->row + 1);
	fd = open(file, O_RDONLY);
	map_skip_element(fd, index);
	while (get_next_line(fd, &line))
	{
		if (ft_strlen(line) < (size_t)map->col)
			map->array[i] = map_padding(line, map->col - ft_strlen(line));
		else
		{
			map->array[i] = ft_strdup(line);
			free(line);
		}
		i++;
	}
	map->array[map->player_pos.y][map->player_pos.x] = '0';
	close(fd);
	free(line);
}