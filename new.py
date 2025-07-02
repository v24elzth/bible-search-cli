# Bible CLI Project - Refactored Version

import csv

# ================= TRANSLATION ====================
translations = {
    "english": {
        "choose_language": "Choose language (indonesia/english): ",
        "menu": [
            "Choose an option:",
            "1. Find Verse",
            "2. Count Keyword",
            "3. Bookmarks",
            "0. Exit"
        ],
        "enter_reference": "Enter reference (e.g., Genesis 1:1): ",
        "verse_not_found": "Verse not found.",
        "enter_keyword": "Enter keyword to search: ",
        "keyword_count": "The keyword '{}' appears {} times.",
        "invalid_option": "Invalid option, please try again.",
        "goodbye": "Goodbye!",
        "confirm_verse_sort" : 'Enter sorting option (a = asc / b = desc): ',
        "bookmarks_menu": [
            "1. See Bookmarks",
            "2. Add Bookmark",
            "3. Update Bookmark",
            "4. Delete Bookmark",
            "0. Back to main menu"
        ],
        "bookmarks": {
            "no_bookmark": "No bookmarks found.",
            "enter_bookmark": "Enter the verse to bookmark: ",
            "bookmark_added": "Bookmark added.",
            "select_bookmark": "Enter the number of the bookmark to update/delete: ",
            "bookmark_updated": "Bookmark updated.",
            "bookmark_deleted": "Bookmark deleted."
        }
    },

    "indonesia": {
        "choose_language": "Pilih bahasa (indonesia/english): ",
        "menu": [
            "Pilih opsi:",
            "1. Cari Ayat",
            "2. Hitung Kata",
            "3. Bookmarks",
            "0. Keluar"
        ],
        "enter_reference": "Masukkan referensi (contoh: Kej 1:1): ",
        "verse_not_found": "Ayat tidak ditemukan.",
        "enter_keyword": "Masukkan kata kunci: ",
        "keyword_count": "Kata kunci '{}' muncul sebanyak {} kali.",
        "invalid_option": "Pilihan tidak valid, coba lagi.",
        "goodbye": "Sampai jumpa!",
        "confirm_verse_sort" : 'Masukkan opsi pengurutan (a = naik / b = turun): ',
        "bookmarks_menu": [
            "1. Lihat Bookmark",
            "2. Tambah Bookmark",
            "3. Ubah Bookmark",
            "4. Hapus Bookmark",
            "0. Kembali ke menu utama"
        ],
        "bookmarks": {
            "no_bookmark": "Tidak ada bookmark.",
            "enter_bookmark": "Masukkan ayat untuk ditandai: ",
            "bookmark_added": "Bookmark ditambahkan.",
            "select_bookmark": "Masukkan nomor bookmark yang ingin diubah/dihapus: ",
            "bookmark_updated": "Bookmark diperbarui.",
            "bookmark_deleted": "Bookmark dihapus."
        }
    }
}

# ==================== CORE FUNCTIONS ====================

def read_csv_file(file_path):
    bibleD = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for col in reader:
            if len(col) >= 5:
                key = f"{col[1]} {col[2]}:{col[3]}"
                bibleD[key] = col[4]
    return bibleD

def quicksort(arr, reverse=False):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot] if not reverse else [x for x in arr if x > pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot] if not reverse else [x for x in arr if x < pivot]
    return quicksort(left, reverse) + middle + quicksort(right, reverse)

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def find_verse(data_dict, reference, sorted_keys):
    idx = binary_search(sorted_keys, reference)
    return data_dict[sorted_keys[idx]] if idx != -1 else None

def count_keyword(data_dict, keyword):
    keyword = keyword.lower()
    return sum(keyword in verse.lower() for verse in data_dict.values())

# ==================== BOOKMARK ====================
def bookmarks_menu(bookmarks, lang):
    trans = translations[lang]["bookmarks"]
    while True:
        print("\n" + "\n".join(translations[lang]["bookmarks_menu"]))
        opt = input(">> ")
        if opt == "1":
            if not bookmarks:
                print(trans["no_bookmark"])
            else:
                for i, bm in enumerate(bookmarks):
                    print(f"{i+1}. {bm}")
        elif opt == "2":
            verse = input(trans["enter_bookmark"])
            bookmarks.append(verse)
            print(trans["bookmark_added"])
        elif opt == "3":
            if not bookmarks:
                print(trans["no_bookmark"])
            else:
                for i, bm in enumerate(bookmarks):
                    print(f"{i+1}. {bm}")
                idx = int(input(trans["select_bookmark"])) - 1
                if 0 <= idx < len(bookmarks):
                    new_verse = input(trans["enter_bookmark"])
                    bookmarks[idx] = new_verse
                    print(trans["bookmark_updated"])
        elif opt == "4":
            if not bookmarks:
                print(trans["no_bookmark"])
            else:
                for i, bm in enumerate(bookmarks):
                    print(f"{i+1}. {bm}")
                idx = int(input(trans["select_bookmark"])) - 1
                if 0 <= idx < len(bookmarks):
                    del bookmarks[idx]
                    print(trans["bookmark_deleted"])
        elif opt == "0":
            break
        else:
            print(translations[lang]["invalid_option"])

# ==================== MAIN ====================
def main():
    lang = input(translations["english"]["choose_language"]).lower()
    lang = lang if lang in ["english", "indonesia"] else "english"
    file_path = "lai_tb.csv" if lang == "indonesia" else "kjv.csv"

    data = read_csv_file(file_path)
    confirm = input(translations[lang]["confirm_verse_sort"])
    sorted_keys = quicksort(list(data.keys()), reverse=(confirm.lower() == 'b'))
    bookmarks = []

    while True:
        print("\n" + "\n".join(translations[lang]["menu"]))
        option = input(">> ")
        if option == "1":
            ref = input(translations[lang]["enter_reference"])
            result = find_verse(data, ref, sorted_keys)
            print(result if result else translations[lang]["verse_not_found"])
        elif option == "2":
            keyword = input(translations[lang]["enter_keyword"])
            count = count_keyword(data, keyword)
            print(translations[lang]["keyword_count"].format(keyword, count))
        elif option == "3":
            bookmarks_menu(bookmarks, lang)
        elif option == "0":
            print(translations[lang]["goodbye"])
            break
        else:
            print(translations[lang]["invalid_option"])

if __name__ == "__main__":
    main()
