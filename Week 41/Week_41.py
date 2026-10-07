# INF201 Week 41 Python exercises
# Student: Christian Bjørklund Seeberg


# Task 1, Flatten a nested list
def flatten(nested):
    """Flattens a nestes list or tuple structure of 
    arbitrary depth into a single flat list.
    Recursively unpacks nested lists and tuples while 
    perserving non-container data
    types as such as int, float, str, bool and None.

    Args:
        nested (list | tuple): The nested sequence structure 
        to flatten. Returns: list: A 1D flat list containing 
        all individual elements in sequence. 
    """
    
    result = []
    for element in nested:
        if isinstance(element, (list, tuple)):
            #Recursive call falltens the next level down
            result.extend(flatten(element))
        else:
            result.append(element)
    return result


def test_flatten():
    """ Runs test cases for the flatten function covering various
    data types and depths.
    """
    assert flatten([1, 2, [3, 4]]) == [1, 2, 3, 4]
    assert flatten(["this", ["is", ["a", "list"]]]) == ["this", "is", "a", "list"]
    assert flatten([]) == []
    assert flatten([[], [[]], ()]) == []
    assert flatten([1, (2, [3, (4,)]), None, True, 2.5, "ab"]) == [1, 2, 3, 4, None, True, 2.5, "ab"]

    # For 10 levels deep
    deep = [1]
    for _ in range(9):
        deep = [deep, 2]
    assert flatten(deep) == [1] + [2] * 9
    print("Task 1 complete")


# Task 2, Process error logs

def process_logfiles(files, outfile):
    """ Reads multiple log files with different text encodings
    and collects valid log lines.
    Parse each specified file using its given encoding, extracts
    lines starting with "[". and outputs all valid entries into
    single file encoding in UTF-8 with BOM.
    Args:
        files (list of tuple): A list of tuples containing
        (file_path, encoding). outfile (str): The target file path
        for the merged log output.
    Returns:
        int: The total count of valid log lines written to the output file.
    """

    count = 0

    with open(outfile, "w", encoding="utf-8-sig") as out:
        for path, encoding in files:
            with open(path, "r", encoding=encoding) as infile:
                for line in infile:
                    line = line.strip()
                    if line.startswith("["):
                        out.write(line + "\n")
                        count += 1
    return count


if __name__ == "__main__":
    test_flatten()

    log_files = [
        ("log_1.txt", "utf-8"),
        ("log_2.txt", "utf-8-sig"),
        ("log_3.txt", "utf-16"),
        ("log_4.txt", "latin-1"),
    ]
    n = process_logfiles(log_files, "output.log")
    print(f"Task 2: wrote {n} lines to output.log")


