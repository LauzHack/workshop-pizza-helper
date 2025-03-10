class Pizza:
    def __init__(self) -> None:
        # Constants for calculation
        self.PIZZA_PER_PARTICIPANT = 0.8
        self.PIZZA_PER_STAFF = 1.0
        self.PIZZA_REDUCTION_PER_WEEK = 0.4
        self.PIZZA_DIVISION_FACTOR = 3.5

        # Pizza distribution ratios
        self.PIZZA_RATIOS = {
            "Gamberetti": 1 / 7,
            "Funghi": 1 / 4,
            "Verde": 1 / 4,
            "Kickiricki": 1 / 4,
            "Prosciutto": 1 / 3,
            "Salame": 1 / 3,
            # Fior di Margherita takes the remainder
        }

        # Default order information
        self.BILLING_INFO = {
            "name": "LauzHack",
            "address": "LauzHack, Station 14, 1015 Lausanne",
            "email": "lauzhack@epfl.ch",
        }

        self.DELIVERY_LOCATION = "Batiment BC, Chem Alan Turing, 1015 Ecublens https://maps.app.goo.gl/NvtF2EbUwyFMev4P6"
        self.PIZZA_SIZE = "large 40cm, sliced"

    def format_pizza_item(self, quantity: int, name: str) -> str:
        """Format a pizza item for the order if quantity > 0."""
        if quantity <= 0:
            return ""
        return f" - {name} x{quantity}\n"

    def calculate_pizza_distribution(self, total_pizzas: int) -> dict:
        """Calculate the distribution of different pizza types."""
        remaining_pizzas = total_pizzas
        distribution = {}

        # Distribute according to ratios
        for pizza_type, ratio in self.PIZZA_RATIOS.items():
            if pizza_type == "Verde" or pizza_type == "Kickiricki":
                # Ensure at least 1 for these types
                quantity = max(int(remaining_pizzas * ratio), 1)
            else:
                quantity = int(remaining_pizzas * ratio)

            distribution[pizza_type] = quantity
            remaining_pizzas -= quantity

        # Assign remaining pizzas to Fior di Margherita
        distribution["Fior di Margherita"] = max(0, remaining_pizzas)

        return distribution

    def get_user_input(
        self, prompt: str, input_type=str | int, default=None, min_value=None
    ):
        """Get and validate user input with error handling."""
        while True:
            try:
                user_input = input(prompt)
                if user_input == "" and default is not None:
                    return default

                # Convert to the appropriate type
                if input_type is int:
                    value = int(user_input)
                    if min_value is not None and value < min_value:
                        print(f"Value must be at least {min_value}. Please try again.")
                        continue
                else:
                    value = user_input

                return value
            except ValueError:
                print("Invalid input. Please try again.")

    def calculate_total_pizzas(self, participants: int, staff: int, weeks: int) -> int:
        """Calculate the total number of pizzas needed."""
        return int(
            (
                participants * self.PIZZA_PER_PARTICIPANT
                + staff * self.PIZZA_PER_STAFF
                - weeks * self.PIZZA_REDUCTION_PER_WEEK
            )
            / self.PIZZA_DIVISION_FACTOR
        )

    def main(self) -> None:
        print("=== Workshop Pizza Order Generator ===\n")

        # Collect order details
        person = self.get_user_input(
            "Who will receive the order? ",
            default="",
        )
        person_message = f"{'I' if person == '' else person} will receive the order."

        phone = self.get_user_input(
            "What is the phone number of the person receiving the order? "
        )
        if not phone:
            print(
                "Warning: No phone number provided. This might cause delivery issues."
            )
        phone_message = f"{person}'s phone number: {phone}"

        # Get event details with validation
        nb_part = self.get_user_input(
            "Enter the number of participants: ", input_type=int, min_value=1
        )
        nb_staff = self.get_user_input(
            "Enter the number of staff members: ", input_type=int, min_value=0
        )
        nb_weeks = self.get_user_input(
            "Enter the number of weeks since the beginning of the semester: ",
            input_type=int,
            min_value=0,
        )

        # Calculate pizza quantities
        total_pizzas = self.calculate_total_pizzas(nb_part, nb_staff, nb_weeks)
        if total_pizzas <= 0:
            print(
                "Warning: The calculation resulted in 0 or negative pizzas. Setting to 1."
            )
            total_pizzas = 1

        print(f"\nCalculated total: {total_pizzas} pizzas")

        # Ask for confirmation or adjustment
        adjustment = self.get_user_input(
            f"Adjust total pizza count? (Press Enter to keep {total_pizzas} or enter new number): ",
            input_type=int,
            default=total_pizzas,
            min_value=1,
        )
        total_pizzas = adjustment

        # Calculate pizza distribution
        pizza_distribution = self.calculate_pizza_distribution(total_pizzas)

        # Format pizza details
        pizza_details = ""
        for pizza_type, quantity in pizza_distribution.items():
            pizza_details += self.format_pizza_item(quantity, pizza_type)

        # Generate the order text
        order_text = f"""Hello Dieci Team!

Thank you for the order last week!

Below is another order we will need today around 19h30.

We would like to pay by invoice.
Billing address:
- name: {self.BILLING_INFO['name']}
- address: {self.BILLING_INFO['address']}
- email: {self.BILLING_INFO['email']}

{person_message}

Delivery details:
- Location: {self.DELIVERY_LOCATION}
- {phone_message}

{total_pizzas} pizzas (all {self.PIZZA_SIZE}):
{pizza_details}
Best regards,

LauzHack committee."""

        # Preview the order
        print("\n=== Order Preview ===")
        print(order_text)
        print("=====================\n")

        # Confirm and save
        confirm = self.get_user_input("Save this order to order.txt? (y/n): ")
        if confirm.lower() in ["y", "yes"]:
            try:
                with open("order.txt", "w") as f:
                    f.write(order_text)
                print("Successfully wrote to order.txt.")
            except Exception as e:
                print(f"Error writing to file: {e}")
        else:
            print("Order was not saved.")


if __name__ == "__main__":
    pizza = Pizza()
    pizza.main()
