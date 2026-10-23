"""Main entry point for Disaster Relief Logistics."""

def show_menu():
    print("========== DISASTER RELIEF LOGISTICS ==========")
    print("1. Location and Supply Trees")
    print("2. AVL Relief-Camp Index")
    print("3. Graph and Route Planning")
    print("4. Minimum Spanning Tree")
    print("5. Scheduling and Cycle Detection")
    print("6. Algorithm Analysis")
    print("7. Run Self-Tests")
    print("0. Exit")

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            from trees import trees_menu
            trees_menu()
        elif choice == "2":
            from avl_expression import avl_expression_menu
            avl_expression_menu()
        elif choice == "3":
            from graph import graph_menu
            graph_menu()
        elif choice == "4":
            from mst import mst_menu
            mst_menu()
        elif choice == "5":
            from scheduling import scheduling_menu
            scheduling_menu()
        elif choice == "6":
            from analysis import analysis_menu
            analysis_menu()
        elif choice == "7":
            from tests import run_tests
            run_tests()
        elif choice == "0":
            print("Exiting Disaster Relief Logistics. Goodbye!")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
