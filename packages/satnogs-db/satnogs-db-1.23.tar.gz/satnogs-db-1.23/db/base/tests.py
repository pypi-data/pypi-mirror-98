"""SatNOGS DB test suites"""
# pylint: disable=R0903
import random
from datetime import datetime, timedelta

import factory
import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import now
from factory import fuzzy

from db.base.models import DATA_SOURCES, DemodData, Mode, Satellite, Telemetry, Transmitter, \
    TransmitterSuggestion

DATA_SOURCE_IDS = [c[0] for c in DATA_SOURCES]


def generate_payload():
    """Create data payloads"""
    payload = '{0:b}'.format(random.randint(500000000, 510000000))
    digits = 1824
    while digits:
        digit = random.randint(0, 1)
        payload += str(digit)
        digits -= 1
    return payload


def generate_payload_name():
    """Create payload names"""
    filename = datetime.strftime(
        fuzzy.FuzzyDateTime(now() - timedelta(days=10), now()).fuzz(), '%Y%m%dT%H%M%SZ'
    )
    return filename


def get_valid_satellites():
    """Returns valid satellites"""
    qs = Transmitter.objects.all()
    satellites = Satellite.objects.filter(transmitters__in=qs).distinct()
    return satellites


class ModeFactory(factory.django.DjangoModelFactory):
    """Mode model factory."""
    name = fuzzy.FuzzyText(length=8)

    class Meta:
        model = Mode


class UserFactory(factory.django.DjangoModelFactory):
    """User model factory"""
    username = factory.Sequence(lambda n: "user_%d" % n)

    class Meta:
        model = get_user_model()


class SatelliteFactory(factory.django.DjangoModelFactory):
    """Sattelite model factory."""
    norad_cat_id = fuzzy.FuzzyInteger(2000, 4000)
    name = fuzzy.FuzzyText()

    class Meta:
        model = Satellite


class TransmitterFactory(factory.django.DjangoModelFactory):
    """Transmitter model factory."""
    description = fuzzy.FuzzyText()
    status = fuzzy.FuzzyChoice(choices=['active', 'inactive', 'invalid'])
    type = fuzzy.FuzzyChoice(choices=['Transmitter', 'Transceiver', 'Transponder'])
    uplink_low = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    uplink_high = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    downlink_low = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    downlink_high = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    downlink_mode = factory.SubFactory(ModeFactory)
    uplink_mode = factory.SubFactory(ModeFactory)
    invert = fuzzy.FuzzyChoice(choices=[True, False])
    baud = fuzzy.FuzzyInteger(4000, 22000, step=1000)
    satellite = factory.SubFactory(SatelliteFactory)
    approved = True
    created = fuzzy.FuzzyDateTime(now() - timedelta(days=30), now() - timedelta(hours=10))
    reviewed = fuzzy.FuzzyDateTime(now() - timedelta(hours=10), now())
    citation = fuzzy.FuzzyText()
    created_by = factory.SubFactory(UserFactory)
    reviewer = factory.SubFactory(UserFactory)

    class Meta:
        model = Transmitter


class TransmitterSuggestionFactory(factory.django.DjangoModelFactory):
    """TransmitterSuggestion model factory."""
    description = fuzzy.FuzzyText()
    status = fuzzy.FuzzyChoice(choices=['active', 'inactive', 'invalid'])
    type = fuzzy.FuzzyChoice(choices=['Transmitter', 'Transceiver', 'Transponder'])
    uplink_low = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    uplink_high = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    downlink_low = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    downlink_high = fuzzy.FuzzyInteger(200000000, 500000000, step=10000)
    downlink_mode = factory.SubFactory(ModeFactory)
    uplink_mode = factory.SubFactory(ModeFactory)
    invert = fuzzy.FuzzyChoice(choices=[True, False])
    baud = fuzzy.FuzzyInteger(4000, 22000, step=1000)
    satellite = factory.SubFactory(SatelliteFactory)
    approved = False
    created = fuzzy.FuzzyDateTime(now() - timedelta(days=30), now())
    citation = fuzzy.FuzzyText()
    created_by = factory.SubFactory(UserFactory)
    service = fuzzy.FuzzyChoice(
        choices=['Amateur', 'Broadcasting', 'Earth Exploration', 'Fixed', 'Inter-satellite']
    )
    coordination = fuzzy.FuzzyChoice(
        choices=['', 'IARU Requested', 'IARU Rejected', 'IARU Coordinated', 'Uncoordinated']
    )

    class Meta:
        model = TransmitterSuggestion


class TelemetryFactory(factory.django.DjangoModelFactory):
    """Telemetry model factory."""
    satellite = factory.SubFactory(SatelliteFactory)
    name = fuzzy.FuzzyText()
    schema = '{}'
    decoder = 'qb50'

    class Meta:
        model = Telemetry


class DemodDataFactory(factory.django.DjangoModelFactory):
    """DemodData model factory."""
    satellite = factory.SubFactory(SatelliteFactory)
    transmitter = factory.SubFactory(TransmitterFactory)
    app_source = fuzzy.FuzzyChoice(choices=DATA_SOURCE_IDS)
    data_id = fuzzy.FuzzyInteger(0, 200)
    payload_frame = factory.django.FileField(filename='data.raw')
    payload_decoded = '{}'
    payload_telemetry = factory.SubFactory(TelemetryFactory)
    station = fuzzy.FuzzyText()
    lat = fuzzy.FuzzyFloat(-20, 70)
    lng = fuzzy.FuzzyFloat(-180, 180)
    timestamp = fuzzy.FuzzyDateTime(now() - timedelta(days=10), now())

    class Meta:
        model = DemodData


@pytest.mark.django_db(transaction=True)
class HomeViewTest(TestCase):
    """
    Simple test to make sure the home page is working
    """
    def test_home_page(self):
        """Tests for a known string in the SatNOGS DB home page template"""
        response = self.client.get('/')
        self.assertContains(response, 'New Satellites')


@pytest.mark.django_db(transaction=True)
class SatelliteViewTest(TestCase):
    """
    Test to make sure the satellite page is working
    """
    satellite = None

    def setUp(self):
        self.satellite = SatelliteFactory()
        self.satellite.save()

    def test_satellite_page(self):
        """Tests for satellite name in a SatNOGS DB satellite page"""
        response = self.client.get('/satellite/%s/' % self.satellite.norad_cat_id)
        self.assertContains(response, self.satellite.name)


@pytest.mark.django_db(transaction=True)
class AboutViewTest(TestCase):
    """
    Test to make sure the about page is working
    """
    def test_about_page(self):
        """Tests for a known string in the SatNOGS DB about page template"""
        response = self.client.get('/about/')
        self.assertContains(response, 'SatNOGS DB is an effort to create an hollistic')
