import json
from typing import Any, Dict, Tuple

import colorama
from colorama import Back, Fore, Style

# Initialize colorama
colorama.init(autoreset=True)


def load_nilai_criteria():
    """Load grading criteria from the nilai.json file"""
    try:
        with open("nilai.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File nilai.json tidak ditemukan!")
        return None
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Format file nilai.json tidak valid!")
        return None
    except Exception as e:
        print(f"{Fore.RED}Error: Terjadi kesalahan saat membaca file: {e}")
        return None


def get_valid_score():
    """Get and validate score input from user"""
    while True:
        try:
            score_input = input(f"{Fore.CYAN}Masukkan nilai (0-100): ")

            # Validate input is not empty
            if not score_input.strip():
                print(f"{Fore.RED}Error: Input tidak boleh kosong!")
                continue

            score = float(score_input)

            # Validate score is within range
            if 0 <= score <= 100:
                return score
            else:
                print(f"{Fore.RED}Error: Nilai harus berada di antara 0 dan 100!")

        except ValueError:
            print(f"{Fore.RED}Error: Input harus berupa angka!")


def determine_grade(
    score: float, criteria: Dict[str, Dict[str, Any]]
) -> Tuple[str | None, Dict[str, Any] | None]:
    """Determine grade based on score and criteria"""
    for grade, info in criteria.items():
        if info["min"] <= score <= info["max"]:
            return grade, info
    return None, None


def get_enhanced_color_code(color_name: str) -> str:
    """Get enhanced color combinations for better visual distinction"""
    color_schemes = {
        "purple": f"{Fore.MAGENTA}{Style.BRIGHT}",  # A grade
        "green": f"{Fore.GREEN}{Style.BRIGHT}",  # B grade
        "blue": f"{Fore.BLUE}{Style.BRIGHT}",  # C grade
        "yellow": f"{Fore.YELLOW}",  # D grade
        "red": f"{Fore.RED}{Style.BRIGHT}",  # E grade
        "cyan": f"{Fore.CYAN}",
        "white": f"{Fore.WHITE}",
    }
    return color_schemes.get(color_name.lower(), f"{Style.RESET_ALL}")


def display_result(score: float, grade: str, info: Dict[str, Any]):
    """Display the result with enhanced colored output based on grade"""
    color_code = get_enhanced_color_code(info["color"])

    print(f"\n{color_code}╔════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{color_code}║            HASIL PENILAIAN             ║{Style.RESET_ALL}")
    print(f"{color_code}╠════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{color_code}║ Nilai    : {score:>25.2f} ║{Style.RESET_ALL}")
    print(f"{color_code}║ Grade    : {grade:>25} ║{Style.RESET_ALL}")
    print(f"{color_code}║ Predikat : {info['predicate']:>25} ║{Style.RESET_ALL}")
    print(f"{color_code}║ Status   : {info['status']:>25} ║{Style.RESET_ALL}")
    print(f"{color_code}╚════════════════════════════════════════╝{Style.RESET_ALL}\n")


def main():
    # Load criteria from JSON
    criteria = load_nilai_criteria()
    if not criteria:
        return

    while True:
        print(
            f"\n{Fore.CYAN}{Back.BLACK}{Style.BRIGHT}==== PROGRAM PENILAIAN KELULUSAN ====\n"
        )

        # Get valid score input
        score = get_valid_score()

        # Determine grade and display result
        grade, info = determine_grade(score, criteria)

        if grade and info:
            display_result(score, grade, info)
        else:
            print(
                f"{Fore.RED}Error: Tidak dapat menentukan grade untuk nilai tersebut!"
            )

        # Ask if the user wants to check another score
        while True:
            continue_choice = input(
                f"{Fore.YELLOW}Apakah ingin mengecek nilai lagi? (y/n): "
            ).lower()
            if continue_choice in ["y", "n"]:
                break
            print(f"{Fore.RED}Error: Masukkan 'y' untuk ya atau 'n' untuk tidak.")

        if continue_choice == "n":
            print(
                f"\n{Fore.CYAN}{Back.BLACK}{Style.BRIGHT}Terima kasih telah menggunakan program ini!"
            )
            break


if __name__ == "__main__":
    main()
