from datetime import date

from logilab.common.testlib import unittest_main
from logilab.common.date import ustrftime

from cubicweb.devtools.testlib import MAILBOX

from utils import ConferenceTC


class TalkNotification(ConferenceTC):
    def setup_database(self):
        self.vreg.config["default-recipients-mode"] = "users"
        super(TalkNotification, self).setup_database()
        with self.admin_access.repo_cnx() as cnx:
            self.user = self.create_user(cnx, u"test_user").eid
            self.reviewer = self.create_user(cnx, u"test_reviewer").eid
            self.admin = self.create_user(cnx, u"test_admin").eid
            cnx.create_entity(
                "EmailAddress",
                address=u"test_user@logilab.fr",
                reverse_use_email=self.user,
            )
            cnx.create_entity(
                "EmailAddress",
                address=u"test_reviewer@logilab.fr",
                reverse_use_email=self.reviewer,
            )
            cnx.create_entity(
                "EmailAddress",
                address=u"test_admin@logilab.fr",
                reverse_use_email=self.admin,
            )

            self.conf = cnx.create_entity(
                u"Conference",
                title=u"conference test",
                url_id=u"conf",
                start_on=ustrftime(date(2010, 3, 1), "%Y/%m/%d"),
                end_on=ustrftime(date(2010, 3, 5), "%Y/%m/%d"),
                take_place_at=self.location,
                description=u"short description",
            ).eid
            self.track = cnx.create_entity(
                u"Track",
                title=u"track test",
                description=u"short track description",
                in_conf=self.conf,
            ).eid
            cnx.commit()

    def test_add_talk(self):
        MAILBOX[:] = []
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity(u"Talk", title=u"Test talk title", in_track=self.track)
            cnx.commit()
            self.assertEqual(len(MAILBOX), 0)
            cnx.execute(
                'SET U in_group G WHERE U login "test_admin", G name "managers"'
            )
            cnx.create_entity(u"Talk", title=u"Test talk title 2", in_track=self.track)
            cnx.commit()
        self.assertEqual(len(MAILBOX), 1)
        self.assertEqual(MAILBOX[0].recipients, ["test_admin@logilab.fr"])
        self.assertEqual(MAILBOX[0].subject, "[conference test] a talk was added")

    def test_update_talk(self):
        MAILBOX[:] = []
        with self.admin_access.repo_cnx() as cnx:
            talk = cnx.create_entity(
                u"Talk", title=u"Test talk title", in_track=self.track
            )
            cnx.commit()
            self.assertEqual(len(MAILBOX), 0)
            talk.cw_set(title=u"new title 1")
            cnx.commit()
            self.assertEqual(len(MAILBOX), 0)
            cnx.execute(
                'SET U in_group G WHERE U login "test_admin", G name "managers"'
            )
            talk.cw_set(title=u"new title 2")
            cnx.commit()
            self.assertEqual(len(MAILBOX), 1)

            MAILBOX[:] = []
            talk.cw_set(reverse_reviews=self.reviewer, reverse_leads=self.user)
            talk.cw_set(title=u"new title 3")
            cnx.commit()
        self.assertEqual(len(MAILBOX), 3)
        MAILBOX.sort(key=lambda x: x.recipients)
        self.assertEqual(
            MAILBOX[0].message.get("Subject"), "[conference test] a talk was updated"
        )
        self.assertEqual(
            [i.recipients[0] for i in MAILBOX[0:3]],
            [
                "test_admin@logilab.fr",
                "test_reviewer@logilab.fr",
                "test_user@logilab.fr",
            ],
        )

    def test_status_talk(self):
        MAILBOX[:] = []
        with self.admin_access.repo_cnx() as cnx:
            talk = cnx.create_entity(
                u"Talk", title=u"Test talk title", in_track=self.track
            )
            cnx.execute(
                'SET U in_group G WHERE U login "test_admin", G name "managers"'
            )
            talk.cw_set(reverse_reviews=self.reviewer, reverse_leads=self.user)
            cnx.commit()
            talk.cw_adapt_to("IWorkflowable").change_state("draft")
            cnx.commit()

            MAILBOX[:] = []
            talk.cw_adapt_to("IWorkflowable").fire_transition("submit your work")
            cnx.commit()
        self.assertEqual(
            MAILBOX[0].message.get("Subject"),
            "[conference test] talk status was updated",
        )
        self.assertEqual(len(MAILBOX), 3)


if __name__ == "__main__":
    unittest_main()
