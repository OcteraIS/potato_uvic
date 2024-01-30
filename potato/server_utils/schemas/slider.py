"""
slider Layout
"""

from .radio import generate_radio_layout

def test_and_get(key, annotation_scheme):
    val = annotation_scheme[key]
    try:
        return int(val)
    except:
        raise Exception(
            'Slider scale %s\'s value for "%s" is not an int' % (annotation_scheme["name"], key)
        )

def generate_slider_layout(annotation_scheme):

    # If the user specified the more complicated likert layout, default to the
    # radio layout
    if "labels" in annotation_scheme:
        return generate_radio_layout(annotation_scheme, horizontal=False)

    # Check all the configurations are present
    for required in ["starting_value", "min_value", "max_value"]:
        if required not in annotation_scheme:
            raise Exception(
                'Slider scale for "%s" did not include %s' % (annotation_scheme["name"], required)
            )

    # Check the values make sense
    min_value = test_and_get("min_value", annotation_scheme)
    max_value = test_and_get("max_value", annotation_scheme)
    starting_value = test_and_get("starting_value", annotation_scheme)

    if min_value >= max_value:
        raise Exception(
            'Slider scale for "%s" must have minimum value < max value (%d >= %d)' \
                % (annotation_scheme["name"], min_value, max_value)
        )

    # Optionally show the labels for the ends of the sliders
    show_labels = True if 'show_labels' not in annotation_scheme \
        else annotation_scheme['show_labels']
    if (show_labels):
        if("min_label" in annotation_scheme):
            min_label = annotation_scheme["min_label"]
        else:
            min_label = str(min_value) 
        if("max_label" in annotation_scheme):
            max_label = annotation_scheme["max_label"]
        else:
            max_label = str(max_label)
    else:
        min_label = ''
        max_label = ''
    name = 'slider:::' + annotation_scheme["name"]
    
    # TODO: Fix the UI alignment so the min/max labels are
    # vertically aligned with the slider bar
    schematic = (
        '<div><form action="/action_page.php">'
        + '  <fieldset> <strong>{description}</strong><br/> '
        + '  <center><span style="flex:1;">{min_label}</span>'
        + '  <input style="position:auto;" type="range" min="{min_value}" max="{max_value}" value="{starting_value}" class="slider" name="{name}" id="{name}" required oninput="updateSliderValue(this)" style="text-align: center;width: 500px;margin:0 auto" validation="required" checked="TRUE">'
        + '  <span style="flex:1;">{max_label}</span>'
        + '  <right>[<span id="sliderValue_{name}" class="slider" validation="required" type="range"></span>]'
        + '</fieldset>\n</form></div><br/>\n'
        + '<script>'
        + '    document.addEventListener("DOMContentLoaded", function() {{'
        + '        updateSliderValue(document.getElementById("{name}"));'
        + '    }});'
        + '    function updateSliderValue(slider) {{'
        + '        document.getElementById("sliderValue_" + slider.id).innerHTML = slider.value;'
        + '        slider.addEventListener("input", function() {{'
        + '            document.getElementById("sliderValue_" + slider.id).innerHTML = slider.value;'
        + '        }});'
        + '        console.log(document.getElementById("sliderValue_" + slider.id).innerHTML);'
        + '    }}'
        + '</script>'
    ).format(description=annotation_scheme["description"],
             min_value=annotation_scheme["min_value"],
             max_value=annotation_scheme["max_value"],
             min_label=min_label,
             max_label=max_label,
             starting_value=annotation_scheme["starting_value"],
             name=name,
             )
             

    key_bindings = []
    
    return schematic, key_bindings
