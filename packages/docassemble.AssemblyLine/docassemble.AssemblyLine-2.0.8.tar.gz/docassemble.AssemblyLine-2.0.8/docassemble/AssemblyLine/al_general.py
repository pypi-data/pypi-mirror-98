from docassemble.base.util import Address, Individual, DAList, date_difference, name_suffix, states_list, comma_and_list, word, comma_list, url_action

##########################################################
# Base classes

class ALAddress(Address):
  # Future-proofing TODO: this class can be used to help handle international addresses in the future.
  # Most likely, ask for international address as just 3 unstructured lines. Key thing is
  # the built-in address object requires some fields to be defined that we don't want to require of
  # international addresses when you want to render it to text.
  pass

class ALAddressList(DAList):
  """Store a list of Address objects"""
  def init(self, *pargs, **kwargs):
    super(ALAddressList, self).init(*pargs, **kwargs)
    self.object_type = ALAddress

  def __str__(self):
    return comma_and_list([item.on_one_line() for item in self])

class ALPeopleList(DAList):
  """Used to represent a list of people. E.g., defendants, plaintiffs, children"""
  def init(self, *pargs, **kwargs):
    super(ALPeopleList, self).init(*pargs, **kwargs)
    self.object_type = ALIndividual

  def names_and_addresses_on_one_line(self, comma_string='; '):
    """Returns the name of each person followed by their address, separated by a semicolon"""
    return comma_and_list([str(person) + ', ' + person.address.on_one_line() for person in self], comma_string=comma_string)

  def familiar(self):
    return comma_and_list([person.name.familiar() for person in self])

  def familiar_or(self):
    return comma_and_list([person.name.familiar() for person in self],and_string=word("or"))

class ALIndividual(Individual):
  """Used to represent an Individual on the assembly line project.
  Two custom attributes are objects and so we need to initialize: `previous_addresses` 
  and `other_addresses`
  """
  def init(self, *pargs, **kwargs):
    super(ALIndividual, self).init(*pargs, **kwargs)
    # Initialize the attributes that are themselves objects. Requirement to work with Docassemble
    # See: https://docassemble.org/docs/objects.html#ownclassattributes
    if not hasattr(self, 'previous_addresses'):
      self.initializeAttribute('previous_addresses', ALAddressList)
    if not hasattr(self, 'other_addresses'):
      self.initializeAttribute('other_addresses', ALAddressList)
    if not hasattr(self, 'mailing_address'):
      self.initializeAttribute('mailing_address',ALAddress)

  def phone_numbers(self):
    nums = []
    if hasattr(self, 'mobile_number') and self.mobile_number:
      nums.append(self.mobile_number + ' (cell)')
    if hasattr(self, 'phone_number') and self.phone_number:
      nums.append(self.phone_number + ' (other)')
    return comma_list(nums)
  
  def merge_letters(self, new_letters):
    # TODO: move to 209A package
    """If the Individual has a child_letters attribute, add the new letters to the existing list"""
    if hasattr(self, 'child_letters'):
      self.child_letters = filter_letters([new_letters, self.child_letters])
    else:
      self.child_letters = filter_letters(new_letters)

  def formatted_age(self):
    dd = date_difference(self.birthdate)
    if dd.years >= 2:
      return '%d years' % (int(dd.years),)
    if dd.weeks > 12:
      return '%d months' % (int(dd.years * 12.0),)
    if dd.weeks > 2:
      return '%d weeks' % (int(dd.weeks),)
    return '%d days' % (int(dd.days),)
  
  # This design helps us translate the prompts for common fields just once
  def name_fields(self, uses_parts=True):
    """
    Return suitable field prompts for a name. 
    """
    if uses_parts:
      return [
        {"label": self.first_name_label, "field": self.attr_name('name.first')},
        {"label": self.middle_name_label, "field": self.attr_name('name.middle'), "required": False},
        {"label": self.last_name_label, "field": self.attr_name("name.last")},
        {"label": self.suffix_label, "field": self.attr_name("name.suffix"), "choices": name_suffix(), "required": False}
      ]
    else:
      # Note: we don't make use of the name.text field for simplicity
      # TODO: this could be reconsidered`, but name.text tends to lead to developer error
      return [
        {"label": self.name_text, "field": self.attr_name('name.first')}
      ]
 
  def address_fields(self, country_code="US", default_state=None, show_country=False):
    """
    Return field prompts for address.
    """
    # TODO: make this more flexible to work w/ homeless individuals and
    # international addresses
    fields = [
      {"label": self.address_address_label, "address autocomplete": True, "field": self.attr_name('address.address')},
      {"label": self.address_unit_label, "field": self.attr_name('address.unit'), "required": False},
      {"label": self.address_city_label, "field": self.attr_name("address.city")},
      {"label": self.address_state_label, "field": self.attr_name("address.state"), "code": "states_list(country_code='{}')".format(country_code), "default": default_state},
      {"label": self.address_zip_label, "field": self.attr_name('address.zip'), "required": False},
    ]
    if show_country:
      fields.append({"label": self.address_country_label, "field": self.attr_name("address.country"), "required": False, "code": "countries_list()", "default": country_code})
      # NOTE: using , "datatype": "combobox" might be nice but does not play together well w/ address autocomplete
    return fields      

  def contact_fields(self):
    """
    Return field prompts for other contact info
    """

def section_links(nav):
  """Returns a list of clickable navigation links without animation."""
  sections = nav.get_sections()
  section_link = []
  for section in sections:
    for key in section:
      section_link.append('[' + section[key] + '](' + url_action(key) + ')' )

  return section_link    

########################################################
# Subject-specific classes

class Landlord(ALIndividual):
  pass

class Tenant(ALIndividual):
  pass

class HousingAuthority(Landlord):
  pass

class Applicant(Tenant):
  pass

class Abuser(ALIndividual):
  pass

class Survivor(ALIndividual):
  pass

########################################################
# Compatibility layer to help with migration

# TODO: consider removing after packages migrated

class VCIndividual(ALIndividual):
  pass

class AddressList(ALAddressList):
  pass

class PeopleList(ALPeopleList):
  pass

########################################################
# Miscellaneous functions needed for baseline questions
# These could go in toolbox but keeping here to reduce packages
# needed for baseline running.

# This one is only used for 209A--should move there along with the combined_letters() method
def filter_letters(letter_strings):
  """Used to take a list of letters like ["A","ABC","AB"] and filter out any duplicate letters."""
  # There is probably a cute one liner, but this is easy to follow and
  # probably same speed
  unique_letters = set()
  if isinstance(letter_strings, str):
    letter_strings = [letter_strings]
  for string in letter_strings:
    if string: # Catch possible None values
      for letter in string:
        unique_letters.add(letter)
  try:
    retval = ''.join(sorted(unique_letters))
  except:
    retval = ''
  return retval

# Note: removed "combined_locations" because it is too tightly coupled to MACourts.py right now

def fa_icon(icon, color="primary", color_css=None, size="sm"):
  """
  Return HTML for a font-awesome icon of the specified size and color. You can reference
  a CSS variable (such as Bootstrap theme color) or a true CSS color reference, such as 'blue' or 
  '#DDDDDD'. Defaults to Bootstrap theme color "primary".
  """
  if not color and not color_css:
    return ':' + icon + ':' # Default to letting Docassemble handle it
  elif color_css:
    return '<i class="fa fa-' + icon + ' fa-' + size + '" style="color:' + color_css + ';"></i>'
  else:
    return '<i class="fa fa-' + icon + ' fa-' + size + '" style="color:var(--' + color + ');"></i>'
