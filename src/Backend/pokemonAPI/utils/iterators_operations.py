def sort_dictionary_descending_order(dictionary: {}) -> {}:
    return {
        k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
    }
