/* *********************************************************************
 * This Original Work is copyright of 51 Degrees Mobile Experts Limited.
 * Copyright 2019 51 Degrees Mobile Experts Limited, 5 Charlotte Close,
 * Caversham, Reading, Berkshire, United Kingdom RG4 7BY.
 *
 * This Original Work is licensed under the European Union Public Licence (EUPL) 
 * v.1.2 and is subject to its terms as set out below.
 *
 * If a copy of the EUPL was not distributed with this file, You can obtain
 * one at https://opensource.org/licenses/EUPL-1.2.
 *
 * The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
 * amended by the European Commission) shall be deemed incompatible for
 * the purposes of the Work and the provisions of the compatibility
 * clause in Article 5 of the EUPL shall not apply.
 * 
 * If using the Work as, or as part of, a network application, by 
 * including the attribution notice(s) required under Article 5 of the EUPL
 * in the end user terms of the application under an appropriate heading, 
 * such notice(s) shall fulfill the requirements of that article.
 * ********************************************************************* */

%include std_string.i
%include std_pair.i
%include std_vector.i
%include std_map.i

/* Iterator for MapStringString. */
%newobject *::getIterator const;
%inline %{
  struct MapStringStringIterator {
    typedef std::map<std::string, std::string> map_t;
    MapStringStringIterator(const map_t& m) : it(m.begin()), map(m) {}
    bool hasNext() const {
      return it != map.end();
    }

    const std::string& getKey() {
      return (*it).first;
    }

    const std::string& getValue() {
      return (*it).second;
    }

    void moveNext() {
      it++;
    }

  private:
    map_t::const_iterator it;
    const map_t& map;
  };
%}
%extend std::map<std::string, std::string> {
  MapStringStringIterator* getIterator() const {
    return new MapStringStringIterator(*$self);
  }
}
