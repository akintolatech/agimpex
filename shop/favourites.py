class Favorites:
    def __init__(self, request):
        self.session = request.session
        favorites = self.session.get('favorites')

        if not favorites:
            favorites = self.session['favorites'] = []

        self.favorites = favorites

    def add(self, product_id):
        product_id = int(product_id)
        if product_id not in self.favorites:
            self.favorites.append(product_id)
            self.save()
            return True
        return False

    def remove(self, product_id):
        product_id = int(product_id)
        if product_id in self.favorites:
            self.favorites.remove(product_id)
            self.save()
            return True
        return False

    def toggle(self, product_id):
        product_id = int(product_id)
        if product_id in self.favorites:
            self.favorites.remove(product_id)
            self.save()
            return False   # now removed
        else:
            self.favorites.append(product_id)
            self.save()
            return True    # now added

    def save(self):
        self.session.modified = True

    def __contains__(self, product_id):
        return int(product_id) in self.favorites

    def __len__(self):
        return len(self.favorites)

    def get_ids(self):
        return self.favorites