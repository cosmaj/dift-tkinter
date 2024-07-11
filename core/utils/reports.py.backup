from jinja2 import Environment, FileSystemLoader
import os
import shutil


def generate_report(current_dir, context):
    # Construct the absolute path to the 'templates' directory
    templates_dir = os.path.join(current_dir, "templates")

    # Define the paths to static files
    css_path = os.path.join(
        current_dir,
        "templates",
        "static_files",
        "tailwind.min.css_1.3.5",
        "cdnjs",
        "tailwind.min.css",
    )
    font_awesome_path = os.path.join(
        current_dir, "templates", "static_files", "fontawesome", "css", "all.css"
    )
    logo_path = os.path.join(
        current_dir, "templates", "static_files", "img", "dift-logo.png"
    )
    try:
        image_name = context["image_name"].split("\\")[-1]
        input_image = os.path.join(current_dir, "input", image_name)
    except Exception as e:
        print(f"Error: {e}")

    try:
        output_image = os.path.join(current_dir, "output_pred", image_name)
    except Exception as e:
        print(f"Error: {e}")

    # Directory for the report output and static files
    report_dir = os.path.join(context["directory"], "report_output")
    # report_dir = os.path.join(current_dir, "report_output")
    static_files_dir = os.path.join(report_dir, "static_files")

    # Ensure the report output directory exists
    os.makedirs(static_files_dir, exist_ok=True)

    # Copy static files to the report output directory
    shutil.copy(css_path, os.path.join(static_files_dir, "tailwind.min.css"))
    shutil.copy(font_awesome_path, os.path.join(static_files_dir, "all.css"))
    shutil.copy(logo_path, os.path.join(static_files_dir, "dift-logo.png"))

    try:
        shutil.copy(input_image, os.path.join(static_files_dir, image_name))
        context["input_image"] = f"static_files/{image_name}"
    except Exception as e:
        print(f"Error while copying input image: {e}")

    try:
        shutil.copy(output_image, os.path.join(static_files_dir, image_name))
        context["output_image"] = f"static_files/{image_name}"
    except Exception as e:
        print(f"Error while copying output image: {e}")

    # Update context with the new paths
    context["css_path"] = "static_files/tailwind.min.css"
    context["font_awesome_path"] = "static_files/all.css"
    context["logo_path"] = "static_files/dift-logo.png"

    # Set up the environment with the absolute path to your templates directory
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Load your template
    template = env.get_template("template.html")

    # Render the template with the context
    html_output = template.render(context)

    # Write the output to a new HTML file in the report directory
    output_file_path = os.path.join(report_dir, "output.html")
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(html_output)

    print(
        f"New HTML file has been created at {output_file_path} with bundled static files."
    )
