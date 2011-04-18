import re

def browser_variants(prop, value):
    definitions = [(prop, value)]

    if prop == "opacity":
        # IE opacity filter
        try:
            value = float(value)
            definitions.append( ("filter", "alpha(opacity={value})".format( value=int(round(value*100)) )) )
        except ValueError:
            pass
    elif prop == "-ms-filter":
        # New IE -ms-filter to old filter
        definitions.append( ("filter", value[1:-1]) )
    elif prop in ["box-orient", "box-pack", "box-align", "box-flex", "background-size", "box-shadow", "border-radius", "transform", "transition", "column-count", "column-gap", "column-width", "resize"]:
        definitions.append( ("-o-"+prop, value) )
        definitions.append( ("-moz-"+prop, value) )
        definitions.append( ("-webkit-"+prop, value) )
    elif prop == "text-overflow":
        definitions.append( ("-o-"+prop, value) )
    elif prop == "display" and value=="box":
        definitions.append( (prop, "-moz-"+value) )
        definitions.append( (prop, "-webkit-"+value) )
    else:
        bradius = re.match(r'^border-([^-]+)-([^-]+)-radius$', prop)
        if bradius:
            definitions.append( ("-moz-border-radius-{y}{x}".format(y=bradius.group(1), x=bradius.group(2)), value) )
            definitions.append( ("-webkit-"+prop, value) )

    for (prop, value) in definitions:
        gradient = re.match(r'^(linear-gradient|radial-gradient)\s*\((.*)\)$', value)
        if gradient:
            function = gradient.group(1)
            params = gradient.group(2)
            definitions.append( (prop, "-o-{func}({params})".format(func=function, params=params)) )
            definitions.append( (prop, "-moz-{func}({params})".format(func=function, params=params)) )
            definitions.append( (prop, "-webkit-{func}({params})".format(func=function, params=params)) )

    return definitions
